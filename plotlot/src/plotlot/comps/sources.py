from __future__ import annotations

from dataclasses import dataclass

from plotlot.comps.models import CompPolicy, CompSubject, SaleEvidence


@dataclass(frozen=True, slots=True)
class SourceResult:
    candidates: tuple[SaleEvidence, ...]
    status: str
    notes: tuple[str, ...]
    source_urls: tuple[str, ...]


def _normalized_county(county: str) -> str:
    normalized = county.strip().casefold()
    suffix = " county"
    return normalized[: -len(suffix)].strip() if normalized.endswith(suffix) else normalized


async def fetch_county_candidates(
    subject: CompSubject,
    policy: CompPolicy,
) -> SourceResult:
    """Route only to pinned official county publishers; unsupported markets abstain."""
    market = (subject.state.strip().upper(), _normalized_county(subject.county))
    if market == ("FL", "miami-dade"):
        from plotlot.comps.county_miami_dade import fetch_miami_dade_candidates

        return await fetch_miami_dade_candidates(subject, policy)
    if market == ("FL", "broward"):
        from plotlot.comps.county_broward import fetch_broward_candidates

        return await fetch_broward_candidates(subject, policy)
    if market == ("FL", "palm beach"):
        from plotlot.comps.county_palm_beach import fetch_palm_beach_candidates

        return await fetch_palm_beach_candidates(subject, policy)
    if market == ("CA", "san diego"):
        return SourceResult(
            (),
            "unsupported",
            (
                "San Diego has no approved automated public sale-price source; "
                "use human-reviewed evidence imports.",
            ),
            (),
        )
    return SourceResult(
        (),
        "unsupported",
        ("No pinned official county comparable-sale source is configured.",),
        (),
    )
