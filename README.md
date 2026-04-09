# Installation and setup of PhyloTree website

## Authors: 
Fabian Kinds  
Tristan Kruithof  
Dennis Kuiper  

## Description of product
The website will be able to accept DNA data in the following forms: fasta file, common name, scientific name.
It will use this to build a phylogenetic tree, which can be modified to show things, like the taxonomie, description and pictures of the different organisms inside the phylogenetic tree.

## How to run the website:
In order to run the website the following tools are needed: Biopython version 1.86, Mega cc version 12.1.2 and ETE4 version 4.4.0
<br>
To start the website up, you need to navigate to the website directory in your console, once there you can run this command to open your website:```python3 app.py``` 
This will then start up the website locally and give you an url you can use to access the website
When opening the website you will be met with the homepage with some information about the website. There is also a specific tools page with information about what each tool is used for.
In order to create your own tree you will first need to login using your email. This is so the tools can use this email to run, so make sure to enter a valid email.
Once this is done you can head over to the create tab to make your own tree or to the compare tree, to compare saved trees.
## Installation of tools:

### Miniconda3 25.3.1
##### Description:
First up we are going to star by making sure conda is installed. You can do this by simply typing ```conda --version``` or ```conda list ``` into you console.
If it says something along the lines of *conda not recognized*, that means conda is not installed yet. If it is installed, tou can continue to the creating a conda envirnoment.
##### Installation steps:
- First up you want to open your console
- Then put these after one another in the command line: 
- Make a directory: ```mkdir -p ~/miniconda3```
- Get latest version: ``wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh``
- ```bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3```
- ``rm ~/miniconda3/miniconda.sh``
- Check installation with steps above.
- If u followed the steps correctly, conda should be installed. If these do not work rework your steps or seek help online yourself or use this link: https://www.anaconda.com/docs/getting-started/miniconda/install#linux

### Creating a conda environment
Now that u have succesfully installed conda, its time to create a conda envirnoment

- First up make sure that your console is still opened.
- Then you will start off by creating the envirnoment using the following command: ``conda env create --file path/requirements.yml``. Make sure to replace the path with the location of the yml file included in the site download under the folder installation.
- Then all you have to do is activate the environment using:``conda activate toolbox_tree``


### MEGA cc 12.1.2
##### Description:
Mega cc is a tool used for the alignment of DNA sequences of species and gives a newick file as output. This newick file can be used to make a phylogenetic tree

##### Installation steps:
Install the download file using the following link: https://www.megasoftware.net/

- Here u select Ubuntu/Debian, Command Line (CC), Mega 12.1 (64-bit) and press the download button
- This brings you to a page where you need to fill in a bit of information, fill this in and press download once more.
- Now a download has started, but this is not the one you need. On the page should also be the text which says something about the standalone m,egacc binary executable. Press the download link next to it.
- This should start a download of a tar.gz file, if not make sure you are actually on an Ubuntu/Debian system and try the previous steps again.
- Once downloaded move the file to the MEGACC directory, located under Tools in the website directory.
- Once placed there, run the following command in the terminal: `tar -xvzf megacc-12.1.2-linux.tar.gz` or replace the last bit with the name of ur file.
- Once this is done successfully you want to make sure you move the megacc file out of this newly created directory into the MEGACC directory. You can delete the rest of the files.
- You can then check if the file is executable. To do so go to the directory your tool is placed and run the follwoing command in the terminal: `ls -l`
- This should give something like `-rw-r--r--r 1 rjans students Feb 27 10:00 megacc`
- Make sure it at least says -rw**x**r--r--. If this is not the case yet use the following command `chmod u+x megacc`
- Now the tool should be functional. To make sure this is actually the case run the following command: `megacc -h`
- If the download was successful it should show a list of possible applications of mega cc and its commands


## Contact
For any questions feel free to send an email to the following addresses:<br>
<a href="mailto:tristankruithof19@gmail.com">Tristan Kruithof</a>: tristankruithof19@gmail.com<br>
<a href="mailto:kindsfabian@ziggo.nl">Fabian Kinds</a>: kindsfabian@ziggo.nl<br>
<a href="mailto:dennismkuiper@outlook.com">Dennis Kuiper</a>: dennismkuiper@outlook.com<br>

## Citation for use of tools
#### For BioPython
Cock PA, Antao T, Chang JT, Chapman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL 
(2009) Biopython: freely available Python tools for computational molecular biology and bioinformatics. 
Bioinformatics, 25, 1422-1423

#### For MAFFT
Rozewicki, J., Li, S., Amada, K. M., Standley, D. M., & Katoh, K. 
(2019). MAFFT-DASH: integrated protein sequence and structural alignment. 
Nucleic Acids Research, 47(W1), W5–W10. https://doi.org/10.1093/nar/gkz342

#### For MEGA CC
Stecher G, Suleski M, Tao Q, Tamura K, and Kumar S 
(2025) Journal of Molecular Evolution https://doi.org/10.1007/s00239-025-10287-z

#### For ETE4 
Jaime Huerta-Cepas, François Serra and Peer Bork. "ETE 3: Reconstruction,
analysis and visualization of phylogenomic data."  Mol Biol Evol (2016) doi:
10.1093/molbev/msw046
