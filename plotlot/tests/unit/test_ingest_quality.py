"""Focused ingestion-quality tests for duplicate cleanup."""

from types import SimpleNamespace

from plotlot.pipeline.ingest import deduplicate_chunks


def _chunk(text: str):
    return SimpleNamespace(text=text)


def test_deduplicate_chunks_collapses_whitespace_equivalent_content():
    chunks = [
        _chunk("Sec. 1. Density standard\n\n10 units per acre"),
        _chunk("  sec. 1. density standard  10 units per acre  "),
        _chunk("Sec. 2. Height standard 35 feet"),
    ]

    result = deduplicate_chunks(chunks)

    assert len(result) == 2
    assert result[0] is chunks[0]
    assert result[1] is chunks[2]


def test_deduplicate_chunks_drops_empty_content():
    assert deduplicate_chunks([_chunk("   "), _chunk("\n\t")]) == []
