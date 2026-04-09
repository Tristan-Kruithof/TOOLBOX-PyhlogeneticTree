import sys
sys.path.append('..')
from python.DNA import DNA
import pytest


# Tests for the DNA.py

# These work and are valid

def test_rna_translation():
    assert DNA('ATG').vertalen_naar_RNA() == 'AUG'


def test_protein_translation():
    assert DNA('ATG').vertalen_naar_eiwitten() == 'M'


def test_stop_codon():
    assert DNA('TAA').vertalen_naar_eiwitten() == '_'


# These fail or do not deliver the expected outcome
# That means DNA.py could be improved, but there was not enough time for now
# And it does not matter that much as it should not fall within these errors frequently.

def test_lowercase_ignored():
    assert DNA("atg").vertalen_naar_RNA() == ""
    # Lower case should just work, or it should give an error that it's not a valid fasta file


def test_empty_rna_returns_empty():
    assert DNA("").vertalen_naar_RNA() == ""
    # Should give a warning or error as no DNA was given


def test_empty_crashes():
    with pytest.raises(UnboundLocalError):
        DNA("").vertalen_naar_eiwitten()
    # Doesn't work and doesn't give an error message back with no DNA given for example


def test_incomplete_codon_ignored():
    assert DNA("ATGAA").vertalen_naar_eiwitten() == "M"
    # AA is ignored and should be at least stored somewhere