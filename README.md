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
- Install python3 if necessary
- Before you can install biopython in Linux, you must first create a virtual environment. First, choose a name for the virtual environment. In the example below, the name is
 virtual_environment_name.
- Go to the location where you want to install the environment. Then use the following syntax in your terminal:
**python3 -m <virtual_environment_name>**

- Next, activate the virtual environment with the following syntax:

**source <virtual_environment_name>/bin/activate**

- Finally, install biopython with the following command:

**pip install biopython==1.86**

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
- If the download was successful it should show a list of possible applications of mega cc and its commands


### ETE4 4.4.0
##### Description:
ETE4 in our case is used for outputting and styling a phylogenetic tree with a newick file as an input.
##### Requirements:
- A linux system is required to run ETE4.
- Miniconda (see installation below)
##### Installation steps:

As of right now conda and miniconda are version: 25.3.1
But you download the latest. If those do not work download the versions above.
- Either use an IDE like pycharm or run this in the commandline.
- If it is not installed, first install miniconda. Check by using either: conda list or conda --version. 
- Follow the steps correctly. If these do not work rework your steps or seek help online yourself or use this link: https://www.anaconda.com/docs/getting-started/miniconda/install#linux
- Put these after one another in the command line: 
- Make a directory: ```mkdir -p ~/miniconda3```
- Get latest version: ``wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh``
- ```bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3```
- ``rm ~/miniconda3/miniconda.sh``
- Check installation with steps above.
- Create a python 3+ environment. The easy way is to do this through a conda environment. 
- Put these in the commandline: ``conda create -n PLACENAME and then conda activate PLACENAME``
- Install ETE4's dependencies like cython and the python dependencies. Do this through conda-forge
- To install cython: ``conda-forge cython``. Then to install the python dependencies: ``pip install flask flask-cors flask-httpauth flask-restful flask-compress sqlalchemy numpy PyQt5`` 
- Clone ETE4 branch: ``git clone -b ete4 https://github.com/etetoolkit/ete ete4``
- ``Build ETE4: cd ete4 && pip install -e .``
- In some cases in linux the gcc library must be installed do this by running: ``conda install -c conda-forge gcc_linux-64``


## Citation for use of tools
#### For ETE4 
Jaime Huerta-Cepas, François Serra and Peer Bork. "ETE 3: Reconstruction,
analysis and visualization of phylogenomic data."  Mol Biol Evol (2016) doi:
10.1093/molbev/msw046
