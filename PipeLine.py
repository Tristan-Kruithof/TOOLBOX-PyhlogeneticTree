from Bio import Entrez
import subprocess

Entrez.email = "fabserdabser8@gmail.com"

names_list = ["cow", "armadillo", "rhinoceros", "HORSE", "CAT", "Lion", "Warthog","pig", "raven", "dolphin", "elephant", "tiger", "siberian tiger", "asian elephant", "african elephant", "borneo dwarf elephant", "plains zebra", "salmon", "cod", "eagle", "ostrich", "ant", "tarantula"]

# correct_names = []
scientific_names = []
multiple_names = []
not_found_names = []
fastas = []
not_found_fastas = []
# for name in names_list:
#     stream = Entrez.espell(term=name)
#     record = Entrez.read(stream)
#     correct_spelled_name = record["CorrectedQuery"]
#
#     if correct_spelled_name == "":
#         correct_spelled_name = name
#
#     correct_names.append(correct_spelled_name)


for name in names_list:
    stream = Entrez.esearch(
        db="taxonomy",
        term=name
    )
    record = Entrez.read(stream)
    stream.close()

    if record["IdList"]:
        taxid = record["IdList"][0]
        stream2 = Entrez.efetch(db="taxonomy", id=taxid)
        record2 = Entrez.read(stream2)
        stream2.close()
        science_name = record2[0]["ScientificName"]

        if science_name not in scientific_names:
            scientific_names.append(science_name)
        else:
            multiple_names.append(science_name)

    else:
        not_found_names.append(name)

print(scientific_names)
print(f"Multiple sub-species, which can not be individually added, where detected form the following species: {multiple_names}")
print(not_found_names)

for name in scientific_names:
    term = f"{name}[Organism] AND (COI[Gene] OR COX1[Gene] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[Sequence Length]"
    stream = Entrez.esearch(db="nucleotide", term=term)
    record = Entrez.read(stream)
    stream.close()

    if record["IdList"]:
        seq_id = record["IdList"][0]
        stream2 = Entrez.efetch(db="nucleotide", id=seq_id, rettype="fasta", retmode="text")
        fasta = stream2.read()
        stream2.close()
        fastas.append(fasta)

    else:
        not_found_fastas.append(name)

with open("sequences.fasta", "w") as f:
    for fasta in fastas:
        f.write(fasta)

print(not_found_fastas)

mafft_in = "C:/Users/Fabian/PyCharmMiscProject/sequences.fasta"
mafft_out = "aligned_sequences.fasta"
mafft_loc = "C:/Users/Fabian/MAFFT"

with open(mafft_out, "w") as f:
    subprocess.run(["C:/Users/Fabian/MAFFT/mafft.bat", "--auto", mafft_in], cwd=mafft_loc, stdout=f, check=True)

mega_in = "C:/Users/Fabian/PyCharmMiscProject/aligned_sequences.fasta"
mega_set = "C:/Users/Fabian/Mega/infer_ML_nucleotide.mao"
mega_out = "newick.nwk"
mega_loc = "C:/Users/Fabian/Mega"


subprocess.run(["megacc", "-a", mega_set, "-d", mega_in, "-o", mega_out], cwd=mega_loc, check=True, capture_output=True)