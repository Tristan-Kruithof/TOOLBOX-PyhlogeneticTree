from Bio import Entrez
import subprocess
import time
import os.path as path
import os
import re
from ete4 import Tree
from ete4.treeview import TreeStyle


#Entrez.email = "superherofabs08@gmail.com"
#Entrez.api_key = "94b49b77b56c715b8dab043b667c611d8408"

class Organisms:
    def __init__(self, method, organisms, gene, email):
        self.common_name = ""
        self.scientific_names = []
        self.fastas = []
        self.multi_fasta = []


        if isinstance(organisms, str):
            organisms = organisms.split(",")

        if method == 1:
            self.common_name = organisms
            print(self.common_name)

        elif method == 2:
            self.scientific_names = organisms
        elif method == 3:
            self.fastas = organisms
        elif method == 4:
            self.multi_fasta = organisms

        Entrez.tool = "PhyloTreePipeline"
        Entrez.email = email
        self.email = email
        self.gene = gene

    def __str__(self):
        if self.common_name:
            return 'Your Animals: {}, Your email: {}'.format(self.common_name, self.email)
        else:
            return "{}".format(self.email)


    def find_scientific_names(self):
        self.scientific_names = []
        self.multiple_names = []
        self.not_found_names = []
        science_name = ""

        for i, name in enumerate(self.common_name):
            time.sleep(1)
            stream = Entrez.esearch(
                db="taxonomy",
                term=name
            )
            record = Entrez.read(stream)
            stream.close()

            if record["IdList"]:
                for taxid in record["IdList"]:
                    stream2 = Entrez.efetch(db="taxonomy", id=taxid)
                    record2 = Entrez.read(stream2)
                    stream2.close()
                    if record2:
                        for item in record2:
                            if science_name and isinstance(science_name, str):
                                science_name = [science_name]
                                science_name += [item["ScientificName"]]

                            elif science_name:
                                science_name += [item["ScientificName"]]

                            else:
                                science_name = item["ScientificName"]

                if science_name not in self.scientific_names:
                    self.scientific_names.append(science_name)
                else:
                    self.multiple_names.append(name)
                    self.common_name.pop(i)
                science_name = ""

            else:
                self.not_found_names.append(name)
                self.common_name.pop(i)
                science_name = ""

        print(self.scientific_names)

    def find_fastas(self):
        self.fastas = []
        self.not_found_fastas = []
        pattern = re.compile("(.+?)\n(.+)", re.DOTALL)


        for i,name in enumerate(self.scientific_names):
            if isinstance(name, str):
                print(name)
                name = name.strip()
                time.sleep(0.5)
                term = f"{name}[Organism] AND {self.gene}"
                stream = Entrez.esearch(db="protein", term=term, retmax=1)
                record = Entrez.read(stream)
                stream.close()

                if record["IdList"]:
                    seq_id = record["IdList"][0]
                    stream2 = Entrez.efetch(db="protein", id=seq_id, rettype="fasta", retmode="text")
                    fasta = stream2.read()
                    stream2.close()
                    fa = re.search(pattern, fasta)
                    new = f">{self.common_name[i]}\n{fa[2]}"
                    self.fastas.append(new)

                else:
                    self.not_found_fastas.append(name)

            else:
                for item in name:
                    print(item)
                    item = item.strip()
                    time.sleep(0.5)
                    term = f"{item}[Organism] AND {self.gene}"
                    stream = Entrez.esearch(db="protein", term=term, retmax=1)
                    record = Entrez.read(stream)
                    stream.close()

                    if record["IdList"]:
                        seq_id = record["IdList"][0]
                        stream2 = Entrez.efetch(db="protein", id=seq_id, rettype="fasta", retmode="text")
                        fasta = stream2.read()
                        stream2.close()
                        fa = re.search(pattern, fasta)
                        new = f">{self.common_name[i]}\n{fa[2]}"
                        self.fastas.append(new)
                        break

                    else:
                        self.not_found_fastas.append(item)


    def make_multi_fasta(self):
        with open("Tools/mafft_input/sequences.fasta", "w") as f:
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

        if self.settings:
            if path.exists(self.output):
                os.remove(self.output)

            subprocess.run([path.abspath("Tools/MEGACC/megacc"), "-a", self.settings, "-d", self.data, "-o", self.output], cwd=self.location, check=True, text=True, capture_output=True)

        else:
            with open(self.output, "w") as f:
                subprocess.run(["mafft", "--auto", self.data], stdout=f, check=True)



def make_tree(shape, newick_file=path.abspath("Tools/ete4_input/newick.nwk")):
    with open(newick_file) as f:
        newick = f.read()
        t = Tree(newick)
        style = TreeStyle()
        style.mode = shape
        style.scale = 500
        return t, style


class Run:
    def __init__(self, email, gene, shape, method=1, organisms=None,
                 location=path.abspath("Tools"), input_mafft=path.abspath("Tools/mafft_input/sequences.fasta"),
                 output_mafft=path.abspath("Tools/mega_input/aligned_sequences.fasta"),input_mega=path.abspath("Tools/mega_input/aligned_sequences.fasta"),
                 output_mega=path.abspath("Tools/ete4_input/newick.nwk"), settings=path.abspath("Tools/infer_ML_amino_acid.mao")):

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
        self.shape = shape


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

        tree, style = make_tree(self.shape)
        tree.render(f"static/pipeline_output/{self.email}tree.png", tree_style= style)


    def fasta_run(self):

        maffie = CC_Tools(self.location, path.abspath("Tools/mafft_input/user_uploads/sequences.fasta"), self.output_mafft)
        maffie.run()

        megurt = CC_Tools(self.location, self.input_mega, self.output_mega, self.settings)
        megurt.run()

        tree, style = make_tree(self.shape)
        tree.render(f"static/pipeline_output/{self.email}tree.png", tree_style=style)


def compare_trees(tree1, tree2):
   t1 = Tree(f"{tree1}")
   t2 = Tree(f"{tree2}")

   rf, max_rf, eff_size, f1, f2, common_nodes, subtrees = t1.robinson_foulds(t2, unrooted_trees=True)

   return {"rf" : rf, "max_rf" : max_rf, "eff_size" : eff_size, "f1" : f1, "f2" : f2, "common_nodes" : common_nodes, "subtrees" : subtrees}


def main():
    time1 = time.time()
    tree = Run("superherofabs08@gmail.com", "BRCA1[GENE] AND 1700:2000[SLEN]")
    tree.standard()

    time2 = time.time()
    print(time2 - time1)


if __name__ == "__main__":
    main()