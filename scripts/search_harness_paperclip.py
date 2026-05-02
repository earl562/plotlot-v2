#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_PROFILE = "docs/research/arxiv-search-profiles/harness-agents.json"
DEFAULT_METADATA = "docs/research/arxiv-abstracts.json"
DEFAULT_URLS = "docs/research/arxiv-urls.txt"
DEFAULT_OUTPUT_JSON = "docs/research/paperclip-harness-search.json"
DEFAULT_OUTPUT_MD = "docs/research/paperclip-harness-search.md"
DEFAULT_OUTPUT_URLS = "docs/research/paperclip-discovery-candidates.txt"


@dataclass
class PaperHit:
    title: str
    url: str | None = None
    abstract: str | None = None
    authors: str | None = None
    paper_id: str | None = None
    source: str | None = None
    date: str | None = None
    arxiv_id: str | None = None
    existing_in_vault: bool = False
    query: str | None = None
    result_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search arXiv via Paperclip for harness-agent topics.")
    p.add_argument("--profile", default=DEFAULT_PROFILE)
    p.add_argument("--query", action="append", default=[])
    p.add_argument("--metadata", default=DEFAULT_METADATA)
    p.add_argument("--existing-urls", default=DEFAULT_URLS)
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--since", default="2024-01-01")
    p.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    p.add_argument("--output-md", default=DEFAULT_OUTPUT_MD)
    p.add_argument("--output-urls", default=DEFAULT_OUTPUT_URLS)
    p.add_argument("--vault-report")
    p.add_argument("--source", default="arxiv")
    return p.parse_args()


def ensure_paperclip_importable() -> None:
    try:
        import gxl_paperclip  # noqa: F401
        return
    except Exception:
        pass

    local_lib = Path.home() / ".paperclip" / "lib"
    if local_lib.exists():
        sys.path.insert(0, str(local_lib))


def load_profile(path_str: str) -> list[str]:
    path = Path(path_str)
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    if isinstance(data, list):
        return [str(x).strip() for x in data if str(x).strip()]
    queries = data.get("queries", []) if isinstance(data, dict) else []
    out: list[str] = []
    for item in queries:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
        elif isinstance(item, dict):
            q = str(item.get("query", "")).strip()
            if q:
                out.append(q)
    return out


def parse_arxiv_id(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s/]+(?:/[^\s/]+)?)", value)
    if m:
        return m.group(1).removesuffix(".pdf")
    m = re.search(r"\barx_([A-Za-z0-9.]+)\b", value)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{4}\.\d{4,5}(?:v\d+)?)\b", value)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Za-z-]+\/\d{7}(?:v\d+)?)\b", value)
    if m:
        return m.group(1)
    return None


def canonical_arxiv_id(value: str | None) -> str | None:
    arxiv_id = parse_arxiv_id(value)
    if not arxiv_id:
        return None
    return re.sub(r"v\d+$", "", arxiv_id)


def load_existing_ids(metadata_path: str, urls_path: str) -> set[str]:
    ids: set[str] = set()
    meta_path = Path(metadata_path)
    if meta_path.exists():
        data = json.loads(meta_path.read_text())
        for item in data.get("items", []):
            arxiv_id = canonical_arxiv_id(item.get("arxivId"))
            if arxiv_id:
                ids.add(arxiv_id)
    url_path = Path(urls_path)
    if url_path.exists():
        for line in url_path.read_text().splitlines():
            arxiv_id = canonical_arxiv_id(line)
            if arxiv_id:
                ids.add(arxiv_id)
    return ids


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def parse_paperclip_output(output: str, query: str, result_id: str | None, existing_ids: set[str]) -> list[PaperHit]:
    text = strip_ansi(output)
    entries = re.split(r"\n(?=\s*\d+\.\s)", text)
    hits: list[PaperHit] = []

    for entry in entries:
        lines = [line.strip() for line in entry.strip().splitlines() if line.strip()]
        if not lines:
            continue
        m = re.match(r"^(\d+)\.\s+(.+)$", lines[0])
        if not m:
            continue

        hit = PaperHit(title=m.group(2).strip(), query=query, result_id=result_id)
        for line in lines[1:]:
            if line.startswith("http://") or line.startswith("https://"):
                hit.url = line
                continue
            if line.startswith('"') and line.endswith('"'):
                hit.abstract = line.strip('"')
                continue
            if "·" in line:
                parts = [part.strip() for part in line.split("·")]
                if parts:
                    hit.paper_id = parts[0]
                if len(parts) >= 2:
                    hit.source = parts[1]
                if len(parts) >= 3:
                    hit.date = parts[2]
                continue
            if hit.authors is None:
                hit.authors = line

        hit.arxiv_id = parse_arxiv_id(hit.url) or parse_arxiv_id(hit.paper_id) or parse_arxiv_id(hit.title)
        canonical_id = canonical_arxiv_id(hit.arxiv_id)
        if canonical_id and canonical_id in existing_ids:
            hit.existing_in_vault = True
        if hit.arxiv_id and not hit.url and re.match(r"^(\d{4}\.\d{4,5}|[A-Za-z-]+\/\d{7})(?:v\d+)?$", hit.arxiv_id):
            hit.url = f"https://arxiv.org/abs/{hit.arxiv_id}"
        hit.raw = {"lines": lines}
        hits.append(hit)
    return hits


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Paperclip arXiv search report")
    lines.append("")
    lines.append(f"Generated: {report['generatedAt']}")
    lines.append(f"Queries: {len(report['queries'])}")
    lines.append(f"Source: {report['source']}")
    lines.append(f"Since: {report['since']}")
    lines.append("")

    lines.append("## New papers not already in the vault")
    lines.append("")
    for hit in report["topNew"]:
        url = hit.get("url") or (f"https://arxiv.org/abs/{hit['arxiv_id']}" if hit.get("arxiv_id") else "")
        lines.append(f"- [{hit.get('arxiv_id') or hit.get('paper_id') or 'unknown'}]({url}) — {hit['title']}")
        lines.append(f"  - query: {hit.get('query')}")
        if hit.get("date"):
            lines.append(f"  - date: {hit['date']}")
        if hit.get("authors"):
            lines.append(f"  - authors: {hit['authors']}")
        if hit.get("abstract"):
            lines.append(f"  - {hit['abstract'][:320]}")
    lines.append("")

    lines.append("## Existing papers already in the vault")
    lines.append("")
    for hit in report["topExisting"]:
        url = hit.get("url") or (f"https://arxiv.org/abs/{hit['arxiv_id']}" if hit.get("arxiv_id") else "")
        lines.append(f"- [{hit.get('arxiv_id') or hit.get('paper_id') or 'unknown'}]({url}) — {hit['title']}")
        lines.append(f"  - query: {hit.get('query')}")
        if hit.get("date"):
            lines.append(f"  - date: {hit['date']}")
    lines.append("")

    lines.append("## By query")
    lines.append("")
    for block in report["byQuery"]:
        lines.append(f"### {block['query']}")
        lines.append("")
        for hit in block["hits"]:
            url = hit.get("url") or (f"https://arxiv.org/abs/{hit['arxiv_id']}" if hit.get("arxiv_id") else "")
            badge = "existing" if hit.get("existing_in_vault") else "new"
            lines.append(f"- [{hit.get('arxiv_id') or hit.get('paper_id') or 'unknown'}]({url}) — {hit['title']} — {badge}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    ensure_paperclip_importable()

    try:
        from gxl_paperclip import PaperclipClient
        from gxl_paperclip.client.errors import AuthError
    except Exception as exc:
        print(f"Paperclip SDK import failed: {exc}", file=sys.stderr)
        return 2

    queries = load_profile(args.profile) + args.query
    queries = [q.strip() for q in queries if q and q.strip()]
    seen: set[str] = set()
    queries = [q for q in queries if not (q in seen or seen.add(q))]
    if not queries:
        print("No queries configured.", file=sys.stderr)
        return 2

    existing_ids = load_existing_ids(args.metadata, args.existing_urls)

    try:
        client = PaperclipClient.from_env()
    except AuthError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    by_query: list[dict[str, Any]] = []
    all_hits: list[PaperHit] = []

    for query in queries:
        result = client.search(query, limit=args.limit, source=args.source, since=args.since)
        hits = parse_paperclip_output(result.output, query, result.result_id, existing_ids)
        by_query.append(
            {
                "query": query,
                "resultId": result.result_id,
                "rawOutput": result.output,
                "hits": [asdict(hit) for hit in hits],
            }
        )
        all_hits.extend(hits)

    new_hits = [hit for hit in all_hits if not hit.existing_in_vault]
    existing_hits = [hit for hit in all_hits if hit.existing_in_vault]

    def dedupe(items: list[PaperHit]) -> list[PaperHit]:
        seen_keys: set[str] = set()
        out: list[PaperHit] = []
        for item in items:
            key = item.arxiv_id or item.url or item.title
            if key in seen_keys:
                continue
            seen_keys.add(key)
            out.append(item)
        return out

    top_new = dedupe(new_hits)[: args.limit]
    top_existing = dedupe(existing_hits)[: args.limit]

    report = {
        "generatedAt": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "source": args.source,
        "since": args.since,
        "queries": queries,
        "byQuery": by_query,
        "topNew": [asdict(hit) for hit in top_new],
        "topExisting": [asdict(hit) for hit in top_existing],
    }

    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_urls).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(report, indent=2) + "\n")
    md = render_markdown(report)
    Path(args.output_md).write_text(md)
    if args.vault_report:
        Path(args.vault_report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.vault_report).write_text(md)

    urls = []
    for hit in top_new:
        if hit.arxiv_id:
            urls.append(f"https://arxiv.org/abs/{hit.arxiv_id}")
        elif hit.url:
            urls.append(hit.url)
    Path(args.output_urls).write_text("\n".join(urls) + ("\n" if urls else ""))

    print(json.dumps({
        "queries": len(queries),
        "topNew": len(top_new),
        "topExisting": len(top_existing),
        "outputJson": args.output_json,
        "outputMd": args.output_md,
        "outputUrls": args.output_urls,
        "vaultReport": args.vault_report,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
