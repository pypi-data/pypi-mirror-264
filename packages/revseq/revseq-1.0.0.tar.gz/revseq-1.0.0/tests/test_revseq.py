import hypothesis.strategies as st
import pytest
from hypothesis import example, given, settings

from revseq import revseq


@settings(deadline=None)
@given(x=st.text(alphabet=["A", "G", "C", "T", "a", "g", "c", "t"], min_size=1))
@example(x="AAAGGTCC")
def test_hypo_revseq(x) -> None:
    revseq(x, rev=True, comp=True)


@pytest.fixture
def test_seq() -> str:
    return "CCCAACCCTGCGACTTCATTGCACACGCGATCTAGTG"


@pytest.fixture
def rev_comp_output() -> str:
    return "CACTAGATCGCGTGTGCAATGAAGTCGCAGGGTTGGG"


@pytest.fixture
def rev_output() -> str:
    return "GTGATCTAGCGCACACGTTACTTCAGCGTCCCAACCC"


@pytest.fixture
def comp_output() -> str:
    return "GGGTTGGGACGCTGAAGTAACGTGTGCGCTAGATCAC"


def test_rev_comp(test_seq: str, rev_comp_output: str) -> None:
    assert revseq(test_seq, rev=True, comp=True) == rev_comp_output


def test_rev(test_seq: str, rev_output: str) -> None:
    assert revseq(test_seq, rev=True, comp=False) == rev_output


def test_comp(test_seq: str, comp_output: str) -> None:
    assert revseq(test_seq, rev=False, comp=True) == comp_output
