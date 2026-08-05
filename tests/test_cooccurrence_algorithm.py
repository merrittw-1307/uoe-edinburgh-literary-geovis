"""
Self-contained test of the document-level co-occurrence method described in
dissertation Finding 3 (Section 3.4): for each document, every pair of
distinct places mentioned in it has its co-occurrence count incremented by
one. This re-implements that exact method against a small synthetic corpus
(no project data files needed) to verify the algorithm itself, independent
of the real corpus.
"""
from collections import Counter
from itertools import combinations


def document_level_cooccurrence(documents: dict[str, set[str]]) -> Counter:
    """documents: {document_id: {place names mentioned in it}}."""
    counts = Counter()
    for places in documents.values():
        for a, b in combinations(sorted(places), 2):
            counts[(a, b)] += 1
    return counts


def test_two_places_in_the_same_document_co_occur():
    docs = {"book1": {"Leith", "Princes Street"}}
    counts = document_level_cooccurrence(docs)
    assert counts[("Leith", "Princes Street")] == 1


def test_weight_counts_distinct_documents_not_mentions():
    # "Leith" and "Princes Street" appear together in 3 books; the fact that
    # a place might be mentioned many times within one book must not inflate
    # the weight beyond the number of distinct shared documents.
    docs = {
        "book1": {"Leith", "Princes Street"},
        "book2": {"Leith", "Princes Street"},
        "book3": {"Leith", "Princes Street", "Old Town"},
    }
    counts = document_level_cooccurrence(docs)
    assert counts[("Leith", "Princes Street")] == 3
    assert counts[("Leith", "Old Town")] == 1
    assert counts[("Old Town", "Princes Street")] == 1


def test_places_in_different_documents_never_co_occur():
    docs = {
        "book1": {"Leith"},
        "book2": {"Old Town"},
    }
    counts = document_level_cooccurrence(docs)
    assert len(counts) == 0


def test_single_place_document_produces_no_pairs():
    docs = {"book1": {"Leith"}}
    counts = document_level_cooccurrence(docs)
    assert len(counts) == 0


def test_sentence_level_granularity_degenerates_to_zero_pairs():
    # Dissertation Finding 3: sentence-level co-occurrence yields zero pairs
    # because no sentence in the corpus contains more than one location
    # mention. Modelling "documents" as individual sentences with at most
    # one place each reproduces that degenerate case directly.
    sentence_level_docs = {
        "book1-sentence1": {"Leith"},
        "book1-sentence2": {"Princes Street"},
        "book2-sentence1": {"Old Town"},
    }
    counts = document_level_cooccurrence(sentence_level_docs)
    assert len(counts) == 0


def test_raising_the_weight_threshold_reduces_pair_count():
    docs = {
        "book1": {"A", "B"},
        "book2": {"A", "B"},
        "book3": {"A", "B"},
        "book4": {"A", "C"},
    }
    counts = document_level_cooccurrence(docs)
    at_weight_1 = {pair for pair, w in counts.items() if w >= 1}
    at_weight_2 = {pair for pair, w in counts.items() if w >= 2}
    assert at_weight_1 == {("A", "B"), ("A", "C")}
    assert at_weight_2 == {("A", "B")}
    assert len(at_weight_2) < len(at_weight_1)
