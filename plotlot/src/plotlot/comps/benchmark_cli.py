import argparse
from collections.abc import Sequence
from dataclasses import replace
from json import JSONDecodeError
from pathlib import Path

import anyio
import httpx
from pydantic import TypeAdapter, ValidationError

from plotlot.comps.arcgis import ArcGISResponseError
from plotlot.comps.benchmark import (
    LAUNCH_MARKETS,
    BenchmarkCase,
    BenchmarkRun,
    BenchmarkSummary,
    assess_run,
    summarize_case,
)
from plotlot.comps.models import CompPolicy
from plotlot.comps.qualification import qualify_comps
from plotlot.comps.sources import SourceResult, fetch_county_candidates
from plotlot.property import lookup_property, registered_counties


async def run_case(case: BenchmarkCase, policy: CompPolicy) -> BenchmarkSummary:
    runs: list[BenchmarkRun] = []
    for _ in range(2):
        identity = "identity_unresolved"
        subject = case.subject
        if subject.county.casefold() not in registered_counties():
            identity = "identity_provider_unsupported"
        else:
            try:
                with anyio.fail_after(25):
                    record = await lookup_property(
                        subject.address,
                        subject.county,
                        state=subject.state,
                        lat=subject.latitude,
                        lng=subject.longitude,
                    )
                if record is not None:
                    identity = (
                        "matched" if record.folio == subject.parcel_id else "identity_mismatch"
                    )
            except TimeoutError:
                identity = "identity_timeout"
            except (httpx.HTTPError, ValidationError, JSONDecodeError, ArcGISResponseError):
                identity = "identity_unavailable"
        try:
            with anyio.fail_after(45):
                source = await fetch_county_candidates(subject, policy)
        except TimeoutError:
            source = SourceResult((), "timeout", ("Benchmark deadline exceeded.",), ())
        except (httpx.HTTPError, ValidationError, JSONDecodeError, ArcGISResponseError) as error:
            source = SourceResult(
                (), "unavailable", (f"Source failed: {type(error).__name__}.",), ()
            )
        result = qualify_comps(subject, source.candidates, policy)
        run = assess_run(case, source, result)
        if identity != "matched":
            run = replace(run, blockers=(*run.blockers, identity))
        runs.append(run)
    return summarize_case(case, tuple(runs))


async def run_benchmark(cases: tuple[BenchmarkCase, ...], policy: CompPolicy) -> int:
    adapter = TypeAdapter(BenchmarkSummary)
    summaries: list[BenchmarkSummary] = []
    for case in cases:
        summary = await run_case(case, policy)
        summaries.append(summary)
        print(adapter.dump_json(summary).decode(), flush=True)
    return 0 if all(summary.ready for summary in summaries) else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run two bounded, credential-free property/comp probes per launch county. "
        "JSON lines report blockers; exit 1 means the benchmark is not ready, not a crash."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--as-of", required=True, help="fixed YYYY-MM-DD evaluation date")
    arguments = parser.parse_args(argv)
    try:
        cases = TypeAdapter(tuple[BenchmarkCase, ...]).validate_json(arguments.cases.read_bytes())
        policy = CompPolicy(as_of=arguments.as_of, radius_miles=3, months=12)
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    markets = {(case.subject.state, case.subject.county) for case in cases}
    if markets != LAUNCH_MARKETS or len(cases) != len(LAUNCH_MARKETS):
        parser.error("cases must contain exactly one property for each of the six launch counties")
    if any(
        not case.subject.address.strip() or not case.identity_source_url.strip() for case in cases
    ):
        parser.error("each property requires an address and independent identity source URL")
    return anyio.run(run_benchmark, cases, policy)


if __name__ == "__main__":
    raise SystemExit(main())
