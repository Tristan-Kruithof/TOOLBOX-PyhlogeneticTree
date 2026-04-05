from Bio import Entrez
import subprocess
import time
import os.path as path
#from ete4 import Tree
import python.login






class Organisms:
    def __init__(self, type, input, email):
        if type == 1:
            input2 = input.split(",")
            self.common_name = input2
            print(self.common_name)
        elif type == 2:
            self.scientific_name = input
        elif type == 3:
            self.fastas = input
        elif type == 4:
            self.multi_fasta = input

        Entrez.email = email

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

        print(self.scientific_names)

    def find_fastas(self):
        self.fastas = []
        self.not_found_fastas = []

        for name in self.scientific_names:
            time.sleep(0.4)
            term = f"{name}[Organism] AND (COI[Gene] OR COX1[Gene] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[Sequence Length]"
            stream = Entrez.esearch(db="nucleotide", term=term)
            record = Entrez.read(stream)
            stream.close()

<<<<<<< HEAD
        for i,name in enumerate(self.scientific_names):
            if isinstance(name, str):
                print(name)
                name = name.strip()
                time.sleep(0.5)
                term = f"{name}[Organism] AND {self.gene}"
                stream = Entrez.esearch(db="nucleotide", term=term, retmax=1)
                record = Entrez.read(stream)
                stream.close()

                if record["IdList"]:
                    seq_id = record["IdList"][0]
                    stream2 = Entrez.efetch(db="protein", id=seq_id, rettype="fasta", retmode="text")
                    fasta = stream2.read()
                    stream2.close()
                    fa = re.search(pattern, fasta)
                    new = f"{self.common_name[i]}\n{fa[2]}"
                    self.fastas.append(new)

                else:
                    self.not_found_fastas.append(name)

            else:
                for item in name:
                    print(item)
                    item = item.strip()
                    time.sleep(0.5)
                    term = f"{item}[Organism] AND {self.gene}"
                    stream = Entrez.esearch(db="nucleotide", term=term, retmax=1)
                    record = Entrez.read(stream)
                    stream.close()

                    if record["IdList"]:
                        seq_id = record["IdList"][0]
                        stream2 = Entrez.efetch(db="protein", id=seq_id, rettype="fasta", retmode="text")
                        fasta = stream2.read()
                        stream2.close()
                        fa = re.search(pattern, fasta)
                        new = f"{self.common_name[i]}\n{fa[2]}"
                        self.fastas.append(new)
                        break

                    else:
                        self.not_found_fastas.append(item)
=======
            if record["IdList"]:
                seq_id = record["IdList"][0]
                stream2 = Entrez.efetch(db="nucleotide", id=seq_id, rettype="fasta", retmode="text")
                fasta = stream2.read()
                stream2.close()
                self.fastas.append(fasta)

            else:
                self.not_found_fastas.append(name)
>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b

        print(self.fastas)

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
            subprocess.run(["rm", self.output])
            subprocess.run([path.abspath("Tools/MEGACC/megacc"), "-a", self.settings, "-d", self.input, "-o", self.output], cwd=self.location, check=True, text=True, capture_output=True)

        else:
            with open(self.output, "w") as f:
                subprocess.run(["mafft", "--auto", self.input], stdout=f, check=True)


def boom():
    return Tree(open(path.abspath("Tools/newick.nwk")).read())


def compare_trees(tree1, tree2):
    t1 = Tree(f"{tree1}")
    t2 = Tree(f"{tree2}")
    rf, max_rf, eff_size, f1, f2, common_nodes, subtrees = t1.compare(t2)

<<<<<<< HEAD
        if organisms is None:
            organisms = ["Elephant", "FAKE_ANIMAL", "Pig", "horse", "Lion", "Tiger"]
        # Location
        self.location = location
        # Gene
        self.gene = gene
        # Input and output for mafft
        self.input_mafft = input_mafft
        self.output_mafft = output_mafft
        # Input and output for mega
        self.input_mega = input_mega
        self.output_mega = output_mega
        # Tool parameters
        self.settings = settings
        self.method = method
        self.organisms = organisms
        self.email = email


    def standard(self, method=None, organisms=None):
        method = method or self.method
        organisms = organisms or self.organisms

        route = Organisms(method, organisms, self.gene, self.email)
        route.find_scientific_names()
        route.find_fastas()
        route.make_multi_fasta()

        maffie = CC_Tools(self.location, self.input_mafft, self.output_mafft)
        maffie.run()

        megurt = CC_Tools(self.location, self.input_mega, self.output_mega, self.settings)
        megurt.run()

        tree = make_tree()
        tree.render(f"static/pipeline_output/{self.email}_tree.png")


    def fasta_run(self):

        maffie = CC_Tools(self.location, path.abspath("Tools/mafft_input/user_uploads/sequences.fasta"), self.output_mafft)
        maffie.run()

        megurt = CC_Tools(self.location, self.input_mega, self.output_mega, self.settings)
        megurt.run()

        tree = make_tree()
        tree.render(f"static/pipeline_output/{self.email}_tree.png")


def compare_trees(tree1, tree2):
   t1 = Tree(f"{tree1}")
   t2 = Tree(f"{tree2}")

   rf, max_rf, eff_size, f1, f2, common_nodes, subtrees = t1.robinson_foulds(t2, unrooted_trees=True)

   return {"rf" : rf, "max_rf" : max_rf, "eff_size" : eff_size, "f1" : f1, "f2" : f2, "common_nodes" : common_nodes, "subtrees" : subtrees}
=======
    return f"Normalized RF:, {rf / max_rf}"
>>>>>>> 6e46949fe8d1b8d8fa7a3bfa6ad6b700bdb26b4b


def main():
    time1 = time.time()
    type = 1
    what = int(type)
    ins = "Elephant, Pig, Cow, horse, Lion, Tiger"

    Route = Organisms(what, ins)
    Route.find_scientific_names()
    Route.find_fastas()
    Route.make_multi_fasta()

    Maffie = CC_Tools(path.abspath("Tools"),path.abspath("Tools/sequences.fasta"),path.abspath("Tools/aligned_sequences.fasta"))
    Maffie.run()

    Megurt = CC_Tools(path.abspath("Tools"),path.abspath("Tools/aligned_sequences.fasta"), path.abspath("Tools/newick.nwk"),path.abspath("Tools/infer_ML_nucleotide.mao"))
    Megurt.run()

    Boom = Tree(open(path.abspath("Tools/newick.nwk")).read())
    time2 = time.time()
    print(time2 - time1)
    Boom.show()



if __name__ == "__main__":
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