"""
pipeline.py

Calls the tools: biopython, mafft, mega cc and ete4
the makeup our tool pipeline.

Auth: Fabian Kinds, Tristan Kruithof
Date: 10/04/2026
Version: 1.0
PEP-8:
"""

import os.path as path
import os
from Bio import Entrez
import subprocess
import time
import re
from ete4 import Tree
from ete4.treeview import TreeStyle


class Organisms:
    """
    Contains names of organisms and is used to create a multi-fasta
    """
    def __init__(self, method, organisms, gene, email, form):
        """
        Sets information about the organisms, genes and used email

        :param method: Context to incoming organisms
        :param organisms: List of organisms
        :param gene: Gene name
        :param email: Email address
        :param form: If gene is nucleotide or protein based
        """
        self.common_name = ""
        self.scientific_names = []
        self.fastas = []
        self.multi_fasta = []

        # Checks if input is string or something else
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

        # Sets up Entrez data
        Entrez.tool = "PhyloTreePipeline"
        Entrez.email = email
        self.email = email
        self.gene = gene
        self.form = form


    def __str__(self):
        """
        Makes returned string based on given organisms and email
        """
        if self.common_name:
            return 'Your Animals: {}, Your email: {}'.format(self.common_name, self.email)
        else:
            return "{}".format(self.email)


    def find_scientific_names(self):
        """
        Makes contact with NCBI to retrieve scientifi names of given organisms
        """
        self.scientific_names = []
        self.multiple_names = []
        self.not_found_names = []
        science_name = ""

        # Loop through all organisms
        for i, name in enumerate(self.common_name):
            #Makes it so NCBI doenst time-out
            time.sleep(1)

            #Searches NCBI for data and saves it
            stream = Entrez.esearch(
                db="taxonomy",
                term=name
            )
            record = Entrez.read(stream)
            stream.close()

            if record["IdList"]:
                for taxid in record["IdList"]:
                    #Searches NCBI with ID to gather data about species
                    stream2 = Entrez.efetch(db="taxonomy", id=taxid)
                    record2 = Entrez.read(stream2)
                    stream2.close()
                    if record2:
                        #If data was found it will save it in a variable
                        for item in record2:
                            #If NCBI returns multiple scientifi names, they will all be saved.
                            if science_name and isinstance(science_name, str):
                                science_name = [science_name]
                                science_name += [item["ScientificName"]]

                            elif science_name:
                                science_name += [item["ScientificName"]]

                            else:
                                science_name = item["ScientificName"]

                #If scientifi name wasnt already saved, it will be saved. Otherwise it will be dumped in a duplicate variable and name will be popped form organisms
                if science_name not in self.scientific_names:
                    self.scientific_names.append(science_name)
                else:
                    self.multiple_names.append(name)
                    self.common_name.pop(i)
                science_name = ""

            #If NCBI didnt return anything name will be added to not found and removed from list
            else:
                self.not_found_names.append(name)
                self.common_name.pop(i)
                science_name = ""

    def find_fastas(self):
        """
        Makes contact with NCBI to get the DNA or Protein sequences from given organisms
        """
        self.fastas = []
        self.not_found_fastas = []
        pattern = re.compile("(.+?)\n(.+)", re.DOTALL)


        for i,name in enumerate(self.scientific_names):
            if isinstance(name, str):
                print(name)
                name = name.strip()
                time.sleep(0.5)
                term = f"{name}[Organism] AND {self.gene}"
                stream = Entrez.esearch(db=self.form, term=term, retmax=1)
                record = Entrez.read(stream)
                stream.close()

                if record["IdList"]:
                    seq_id = record["IdList"][0]
                    stream2 = Entrez.efetch(db=self.form, id=seq_id, rettype="fasta", retmode="text")
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
                    stream = Entrez.esearch(db=self.form, term=term, retmax=1)
                    record = Entrez.read(stream)
                    stream.close()

                    if record["IdList"]:
                        seq_id = record["IdList"][0]
                        stream2 = Entrez.efetch(db=self.form, id=seq_id, rettype="fasta", retmode="text")
                        fasta = stream2.read()
                        stream2.close()
                        fa = re.search(pattern, fasta)
                        new = f">{self.common_name[i]}\n{fa[2]}"
                        self.fastas.append(new)
                        break

                    else:
                        self.not_found_fastas.append(item)


    def make_multi_fasta(self):
        """
        Combines the DNA or Protein sequences into one multi-fasta file
        """
        with open("Tools/mafft_input/sequences.fasta", "w") as f:
            for fasta in self.fastas:
                f.write(fasta)



class CC_Tools:
    """Used to run the multiple tools"""
    def __init__(self, location, data, output, settings=""):
        """
        Sets information about used tool

        :param location: sets the location of tool
        :param data: sets the location of input data
        :param output: sets location of output data
        :param settings: sets location of settings file
        """
        self.location =location
        self.data = data
        self.output = output
        self.settings = settings

    def __str__(self):
        """
        Makes string based of tool used
        """
        if self.settings:
            return "You're running Mega CC"
        else:
            return "You're running MAFFT"


    def run(self):
        """
        Runs the selected tool
        """
        if self.settings:
            if path.exists(self.output):
                os.remove(self.output)

            subprocess.run([path.abspath("Tools/MEGACC/megacc"), "-a", self.settings, "-d", self.data, "-o", self.output], cwd=self.location, check=True, text=True, capture_output=True)

        else:
            with open(self.output, "w") as f:
                subprocess.run(["mafft", "--auto", self.data], stdout=f, check=True)



def make_tree(shape, newick_file=path.abspath("Tools/ete4_input/newick.nwk")):
    """
    Makes a phylogenetic tree

    :param shape: shape of the tree
    :param newick_file: path to newick file

    :return t: return the tree object
    :return style: return the tree's style
    """
    with open(newick_file) as f:
        newick = f.read()
        t = Tree(newick)
        style = TreeStyle()
        style.mode = shape
        style.scale = 150
        return t, style


def dna_or_protein(gene):
    """
    Determine if sequences will be DNA or Protein

    :param gene: name of used gene

    ;return: returns either protein or nucleotide
    """
    protein = ["(COI[GENE] OR COX1[GENE] OR cytochrome c oxidase subunit 1[Gene Name]) AND 400:800[SLEN]", "BRCA1[GENE] AND 1700:2000[SLEN]", "rbcL[GENE] AND 400:600[SLEN]", "matK[GENE] AND 400:600[SLEN]"]

    if gene in protein:
        return "protein"

    return "nucleotide"


class Run:
    """
    Class called in the app.py to run the pipeline
    """
    def __init__(self, email, gene, shape, sequence, method=1, organisms=None,
                 location=path.abspath("Tools"), input_mafft=path.abspath("Tools/mafft_input/sequences.fasta"),
                 output_mafft=path.abspath("Tools/mega_input/aligned_sequences.fasta"),input_mega=path.abspath("Tools/mega_input/aligned_sequences.fasta"),
                 output_mega=path.abspath("Tools/ete4_input/newick.nwk"), settings=path.abspath("Tools/infer_ML_amino_acid.mao")):
        """
        Sets up all the information needed to run the pipeline

        :param email: email of the user
        :param gene: name of the gene
        :param shape: shape of the tree
        :param method: method to determine what kind of organsims
        :param organisms: organisms to use
        :param location: location of input data
        :param input_mafft: path to input mafft file
        :param output_mafft: path to output mafft file
        :param input_mega: path to input mega file
        :param output_mega: path to output mega file
        :param settings: path to settings file for mega
        """

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

        self.method = method
        self.organisms = organisms
        self.email = email
        self.shape = shape
        self.sequence = sequence
        self.form = dna_or_protein(gene)

        if self.form == "protein":
            self.settings = settings
        else:
            self.settings = path.abspath("Tools/infer_ML_nucleotide.mao")



    def standard(self, method=None, organisms=None):
        method = method or self.method
        organisms = organisms or self.organisms

        route = Organisms(method, organisms, self.gene, self.email, self.form)
        route.find_scientific_names()
        route.find_fastas()
        route.make_multi_fasta()

        maffie = CC_Tools(self.location, self.input_mafft, self.output_mafft)
        maffie.run()

        megurt = CC_Tools(self.location, self.input_mega, self.output_mega, self.settings)
        megurt.run()

        tree, style = make_tree(self.shape)
        tree.render(f"static/pipeline_output/{self.email}_tree.png", tree_style=style, w=1200, units='px', dpi=100)



    def fasta_run(self):
        if self.sequence == "protein":
            self.settings = path.abspath("Tools/infer_ML_amino_acid.mao")
        else:
            self.settings = path.abspath("Tools/infer_ML_nucleotide.mao")

        maffie = CC_Tools(self.location, path.abspath("Tools/mafft_input/user_uploads/sequences.fasta"), self.output_mafft)
        maffie.run()

        megurt = CC_Tools(self.location, self.input_mega, self.output_mega, self.settings)
        megurt.run()

        tree, style = make_tree(self.shape)
        tree.render(f"static/pipeline_output/{self.email}_tree.png", tree_style=style, w=1200, units='px', dpi=100)


def compare_trees(tree1, tree2):
    t1 = Tree(f"{tree1}")
    t2 = Tree(f"{tree2}")

    rf, max_rf, eff_size, f1, f2, common_nodes, subtrees = t1.robinson_foulds(t2, unrooted_trees=True)
    if not max_rf == 0:
        difference = (rf/max_rf)*100
    else:
        difference = "Not determinable"
    return {"rf" : rf, "max_rf" : max_rf, "difference" : f"{difference}%", "eff_size" : eff_size, "f1" : f1, "f2" : f2}


def main():
    tree = Run("superherofabs08@gmail.com", "BRCA1[GENE] AND 1700:2000[SLEN]", "r")
    tree.standard()


if __name__ == "__main__":
    main()