"""
test_pipeline.py

pytests the python file and the class within of PipeLine.py

Auth: Tristan Kruithof
Date: 10/04/2026
Version: 1.0
PEP-8:
"""

import sys
sys.path.append('..')
from PipeLine import dna_or_protein, Run

# Tests that we can do on our pipeline without testing the tool code

# Checks if it returns
def test_protein_or_nucleotide():
    assert dna_or_protein("(COI[GENE] OR COX1[GENE] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[SLEN]") == "protein"

# Tests if unknown_gene gives nucleotide
def test_unknown_gene():
    assert dna_or_protein("UNKNOWN_GENE") == "nucleotide"

# Tests if amino_acid is in settings when these params are given
def test_sets_correct_settings():
    run = Run("test@example.com", "BRCA1[GENE] AND 1700:2000[SLEN]", "r", "")
    assert "amino_acid" in run.settings

# Tests if nucleotide is in settings if these params are given
def test_sets_correct_settings_unknown_gene():
    run = Run("test@example.com", "UNKNOWN_GENE", "r", "")
    assert "nucleotide" in run.settings