from Bio import Entrez
import subprocess
import time
import os.path as path
import os
from ete4 import Tree as ETETree


class Organisms:
    def __init__(self, method, organisms, email):
        self.common_name = ""
        self.scientific_name = []
        self.fastas = []
        self.multi_fasta = []

        if isinstance(organisms, str):
            organisms = organisms.split(",")

        if method == 1:
            self.common_name = organisms
            print(self.common_name)

        elif method == 2:
            self.scientific_name = organisms
        elif method == 3:
            self.fastas = organisms
        elif method == 4:
            self.multi_fasta = organisms

        Entrez.tool = "PhyloTreePipeline"
        Entrez.email = email
        self.email = email


    def __str__(self):
        if self.common_name:
            return 'Your Animals: {}, Your email: {}'.format(self.common_name, self.email)
        else:
            return "{}".format(self.email)


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
            name = name.strip()
            time.sleep(0.3)
            term = f"{name}[ORGN] AND (COI[GENE] OR COX1[GENE] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[SLEN]"
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

        print(self.fastas)

    def make_multi_fasta(self):
        with open("./Tools/sequences.fasta", "w") as f:
            for fasta in self.fastas:
                f.write(fasta)



class CC_Tools:
    def __init__(self, location, data, output, settings=""):
        self.location =location
        self.data = data
        self.output = output
        self.settings = settings

    def __str__(self):
        if self.settings:
            return "You're running Mega CC"
        else:
            return "You're running MAFFT"


    def run(self):
        mafft_path = path.abspath("Tools/mafft-win/mafft.bat")

        if self.settings:
            if path.exists(self.output):
                os.remove(self.output)

            subprocess.run([path.abspath("Tools/MEGACC/megacc.exe"), "-a", self.settings, "-d", self.data, "-o", self.output], cwd=self.location, check=True, text=True, capture_output=True)

        else:
            with open(self.output, "w") as f:
                subprocess.run([mafft_path, "--auto", self.data], stdout=f, check=True)


class Tree(ETETree):
    def __init__(self, newick_file=path.abspath("Tools/newick.nwk")):
        super().__init__(open(newick_file).read())

    def get_tree(self):
        return self


class Run:
    def __init__(self, email, method=1, organisms=None,
                 location=path.abspath("Tools"), input_mafft=path.abspath("Tools/sequences.fasta"),
                 output_mafft=path.abspath("Tools/aligned_sequences.fasta"),input_mega=path.abspath("Tools/aligned_sequences.fasta"),
                 output_mega=path.abspath("Tools/newick.nwk"), settings=path.abspath("Tools/infer_ML_nucleotide.mao")):

        if organisms is None:
            organisms = ["Elephant", "Pig", "Cow", "horse", "Lion", "Tiger"]
        # Location
        self.location = location
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

        route = Organisms(method, organisms, self.email)
        route.find_scientific_names()
        route.find_fastas()
        route.make_multi_fasta()

        maffie = CC_Tools(self.location, self.input_mafft, self.output_mafft)
        maffie.run()

        megurt = CC_Tools(self.location, self.input_mega, self.output_mega, self.settings)
        megurt.run()

        tree = Tree()
        tree.render("static/pipeline_output/tree.png")



#def tree():
#    t = Tree(open(path.abspath("Tools/newick.nwk")).read())
#
#    return t


#def compare_trees(tree1, tree2):
#    t1 = Tree(f"{tree1}")
#    t2 = Tree(f"{tree2}")
#    rf, max_rf, eff_size, f1, f2, common_nodes, subtrees = t1.compare(t2)

#    return f"Normalized RF:, {rf / max_rf}"


def main():
    time1 = time.time()

    tree = Run("fabserdabser@gmail.com")
    tree.standard()

    #what = 1
    #ins = ["Elephant","Pig","Cow","horse","Lion","Tiger"]

    #Route = Organisms(what, ins, "fabserdabser@gmail.com")
    #print(Route)
    #print(Organisms(2, ins, "fabserdabser@gmail.com"))

    #Route.find_scientific_names()
    #Route.find_fastas()
    #Route.make_multi_fasta()

    #Maffie = CC_Tools(path.abspath("Tools"),path.abspath("Tools/sequences.fasta"),path.abspath("Tools/aligned_sequences.fasta"))
    #print(Maffie)
    #Maffie.run()

    #Megurt = CC_Tools(path.abspath("Tools"),path.abspath("Tools/aligned_sequences.fasta"), path.abspath("Tools/newick.nwk"),path.abspath("Tools/infer_ML_nucleotide.mao"))
    #print(Megurt)
    #Megurt.run()

 #   Boom = Tree(open(path.abspath("Tools/newick.nwk")).read())
    time2 = time.time()
    print(time2 - time1)
#    Boom.show()



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