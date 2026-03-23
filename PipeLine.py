from Bio import Entrez
import subprocess
import time
import os.path as path
from ete3 import Tree




Entrez.email = "fabserdabser8@gmail.com"

#type = 1
#input = ["cow", "armadillo", "rhinoceros", "HORSE", "CAT", "Lion", "Warthog","pig", "raven", "dolphin", "elephant", "tiger", "siberian tiger", "asian elephant", "african elephant", "borneo dwarf elephant", "plains zebra", "salmon", "cod", "eagle", "ostrich", "ant", "tarantula"]
#["cow", "armadillo", "rhinoceros", "HORSE", "CAT", "Lion", "Warthog","pig", "raven", "dolphin", "elephant", "tiger", "siberian tiger", "asian elephant", "african elephant", "borneo dwarf elephant", "plains zebra", "salmon", "cod", "eagle", "ostrich", "ant", "tarantula"]

# correct_names = []
#scientific_names = []
#multiple_names = []
#not_found_names = []
#fastas = []
#not_found_fastas = []
# for name in names_list:
#     stream = Entrez.espell(term=name)
#     record = Entrez.read(stream)
#     correct_spelled_name = record["CorrectedQuery"]
#
#     if correct_spelled_name == "":
#         correct_spelled_name = name
#
#     correct_names.append(correct_spelled_name)


class Organisms():
    def __init__(self, type, input):
        if type == 1:
            input2 = input.split(",")
            self.common_name = input2
        elif type == 2:
            self.scientific_name = input
        elif type == 3:
            self.fastas = input
        elif type == 4:
            self.multi_fasta = input

    def find_scientific_names(self):
        self.scientific_names = []
        self.multiple_names = []
        self.not_found_names = []

        for name in self.common_name:
            time.sleep(0.4)
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
                if record2:
                    science_name = record2[0]["ScientificName"]

                if science_name not in self.scientific_names:
                    self.scientific_names.append(science_name)
                else:
                    self.multiple_names.append(name)

            else:
                self.not_found_names.append(name)

    def find_fastas(self):
        self.fastas = []
        self.not_found_fastas = []

        for name in self.scientific_names:
            time.sleep(0.4)
            term = f"{name}[Organism] AND (COI[Gene] OR COX1[Gene] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[Sequence Length]"
            stream = Entrez.esearch(db="nucleotide", term=term)
            record = Entrez.read(stream)
            stream.close()

            if record["IdList"]:
                seq_id = record["IdList"][0]
                stream2 = Entrez.efetch(db="nucleotide", id=seq_id, rettype="fasta", retmode="text")
                fasta = stream2.read()
                stream2.close()
                self.fastas.append(fasta)

            else:
                self.not_found_fastas.append(name)


    def make_multi_fasta(self):
        with open("./Tools/sequences.fasta", "w") as f:
            for fasta in self.fastas:
                f.write(fasta)






class CC_Tools():
    def __init__(self, location, input, output, settings=False):
        self.location =location
        self.input = input
        self.output = output
        self.settings = settings


    def run(self):
        if self.settings:
            subprocess.run(["megacc", "-a", self.settings, "-d", self.input, "-o", self.output], cwd=self.location, check=False, text=True, capture_output=True)

        else:
            with open(self.output, "w") as f:
                subprocess.run([path.abspath("Tools/MAFFT/mafft.bat"), "--auto", self.input], stdout=f, check=True)




def main():
    type = input("If common names, enter 1! If scientific names, enter 2! If multiple fasta files, enter 3! If one multi-fasta, enter 4!: "
                 "")
    what = int(type)
    ins = input("Enter input: ")


    Route = Organisms(what, ins)
    Route.find_scientific_names()
    Route.find_fastas()
    Route.make_multi_fasta()

    Maffie = CC_Tools(path.abspath("Tools"),path.abspath("Tools/sequences.fasta"),path.abspath("Tools/aligned_sequences.fasta"))
    Maffie.run()

    Megurt = CC_Tools(path.abspath("Tools"),path.abspath("Tools/aligned_sequences.fasta"), path.abspath("Tools/newick.nwk"),path.abspath("Tools/infer_ML_nucleotide.mao"))
    Megurt.run()


main()


# mafft_in = "./Tools/sequences.fasta"
# mafft_out = "aligned_sequences.fasta"
# mafft_loc = "./TOOLBOX-PyhlogeneticTree/Tools"
#
# with open(mafft_out, "w") as f:
#     subprocess.run(["C:/Users/Fabian/MAFFT/mafft.bat", "--auto", mafft_in], cwd=mafft_loc, stdout=f, check=True)
#
# mega_in = "C:/Users/Fabian/PyCharmMiscProject/aligned_sequences.fasta"
# mega_set = "C:/Users/Fabian/Mega/infer_ML_nucleotide.mao"
# mega_out = "newick.nwk"
# mega_loc = "./TOOLBOX-PyhlogeneticTree/Tools"
#
#
# subprocess.run(["megacc", "-a", mega_set, "-d", mega_in, "-o", mega_out], cwd=mega_loc, check=True, capture_output=True)

#for name in names_list:
#     stream = Entrez.esearch(
#         db="taxonomy",
#         term=name
#     )
#     record = Entrez.read(stream)
#     stream.close()
#
#     if record["IdList"]:
#         taxid = record["IdList"][0]
#         stream2 = Entrez.efetch(db="taxonomy", id=taxid)
#         record2 = Entrez.read(stream2)
#         stream2.close()
#         science_name = record2[0]["ScientificName"]
#
#         if science_name not in scientific_names:
#             scientific_names.append(science_name)
#         else:
#             multiple_names.append(science_name)
#
#     else:
#         not_found_names.append(name)
#
# print(scientific_names)
# print(f"Multiple sub-species, which can not be individually added, where detected form the following species: {multiple_names}")
# print(not_found_names)
#
# for name in scientific_names:
#     term = f"{name}[Organism] AND (COI[Gene] OR COX1[Gene] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[Sequence Length]"
#     stream = Entrez.esearch(db="nucleotide", term=term)
#     record = Entrez.read(stream)
#     stream.close()
#
#     if record["IdList"]:
#         seq_id = record["IdList"][0]
#         stream2 = Entrez.efetch(db="nucleotide", id=seq_id, rettype="fasta", retmode="text")
#         fasta = stream2.read()
#         stream2.close()
#         fastas.append(fasta)
#
#     else:
#         not_found_fastas.append(name)
#
# with open("sequences.fasta", "w") as f:
#     for fasta in fastas:
#         f.write(fasta)
#
# print(not_found_fastas)