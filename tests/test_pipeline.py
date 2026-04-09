import sys
sys.path.append('..')
from PipeLine import dna_or_protein, Run


# Tests that we can do on our pipeline without
def protein_or_nucleotide():
    assert dna_or_protein("(COI[GENE] OR COX1[GENE] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[SLEN]") == "protein"


def unknown_gene():
    assert dna_or_protein("UNKNOWN_GENE") == "nucleotide"


def sets_correct_settings():
    run = Run("test@example.com", "BRCA1[GENE] AND 1700:2000[SLEN]", "r")
    assert "amino_acid" in run.settings


def sets_correct_settings_unknown_gene():
    run = Run("test@example.com", "UNKNOWN_GENE", "r")
    assert "nucleotide" in run.settings
