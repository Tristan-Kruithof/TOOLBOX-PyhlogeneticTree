from ete4 import PhyloTree

newick = "((A:0.1,B:0.2)C:0.3,D:0.4);"
tree = PhyloTree(newick, parser=1)


tree.explore()