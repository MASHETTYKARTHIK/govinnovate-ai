"""Tests for the local FAISS-style mock index."""

from backend.repositories.vector_index import MockFaissIndex


def test_vector_index_ranks_matching_document_first() -> None:
    index = MockFaissIndex(["traffic signal congestion", "water leakage sensors"])

    results = index.search("traffic congestion")

    assert results[0][0] == 0
    assert results[0][1] > results[1][1]
