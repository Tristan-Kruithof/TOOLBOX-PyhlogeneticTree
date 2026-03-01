# Installation and setup of PhyloTree website

## Authors: 
Fabian Kinds  
Tristan Kruithof  
Dennis Kuiper  

## Description of product
The website will be able to accept DNA data in the following forms: fasta file, common name, scientific name.
It will use this to build a phyloghenetic tree, which can be modified to show things, like the taxonomie, description and pictures of the different organisms inside the phylogenetic tree.

## How to run the website:
In order to run the website the following tools are needed: Biopython version 1.86, Mega cc version 12.1.2 and ETE4 version 4.4.0
## Installation of tools:

### BioPython 1.86
##### Description:
Tool for getting species information like the taxonomy and fasta files through NCBI's database
##### Installation steps:


### MEGA cc 12.1.2

##### Description:
Mega cc is a tool used for the alignment of DNA sequences of species and gives a newick file as output. This newick file can be used to make a phylogenetic tree

##### Installation steps:
Install the download file using the following link: https://www.megasoftware.net/

- Here u select Ubuntu/Debian, Command Line (CC), Mega 12.1 (64-bit) and press the download button
- This brings you to a page where you need to fill in a bit of information, fill this in and press download once more.
- This should start a download of a tar.gz file, if not make sure you are actually on a Ubuntu/Debian system and try the previous steps again.
- Once downloaded move the file to the directory where you want your tool to live.
- Once placed there, run the following command in the terminal: **tar -xvzf megacc-12.1.2-linux.tar.gz** or replace the last bit with the name of ur file.
- Once this is done successfully you want to make sure the file is executable. To do so go to the directory your tool is placed and run the follwoing command in the terminal: ls -l
- This should give something like **-rw-r--r--r 1 rjans students Feb 27 10:00 megacc**
- Make sure it at least says -rw**x**r--r--. If this is not the case yet use the following command chmod u+x megacc
- Now the tool should be functional. To make sure this is actually the case run the following command: megacc -h
- If the download was successful it should show a list of possible applications of megacc and its commands


### ETE4 4.4.0
##### Description:
Tool for outputting and styling a phylogenetic tree with a newick file as input
##### Installation steps:



