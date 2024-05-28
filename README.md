# Virtual Screening-Analysis

## Python package for Virtual Screening Results Analysis

### VS-Analysis Python package- A powerful toolkit designed to streamline the analysis of virtual screening results.

This package allows you to:

* Find the binding affinities of a selected number of docked compounds,
* sort the binding affinities based on a binding affinity cut-off value (provided by the user) of a selected number of compounds,
* find the specific binding affinity of a docked compound,
* calculate the number of polar hydrogen bonds between the protein and the docked compounds including all poses,
* calculate the distances of these hydrogen bonds, and
* list the names of amino acid residues that are present near the ligand within a specified distance (default distance is 3.2 Angstroms).
* identify whether a ligand is binding within a binding pocket or around a reference ligand in the protein or somewhere else. 

For more information, read [here](https://github.com/MunibaFaiza/VS-Analysis/wiki).

### Usage:

To use <i>vs_analysis.py</i> script, run the following command:

```$ python vs_analysis.py``` 

OR

```$ python3 vs_analysis.py```


Since it is an interactive script, it will prompt the user during its execution.


To use <i>vs_analysis_compound.py</i> script, run the following command:

```$ python vs_analysis_compounds.py <compound-name>``` 

OR

```$ python3 vs_analysis_compounds.py <compound-name>```

***For example,***
You have 50 log files in your directory and you want to fetch the top 20 results/poses sorted with the lowest binding affinities.
Then run the above command and while prompted enter 20. It will provide the top 20 results in the 'output.txt' file.
Remember to enter a valid number, i.e., the number you enter must be less than or equal to the number of files present in the directory.

***NOTE:
This script screens for the log files containing the word 'log' in their filenames.
It is recommended to name your log files along with the name of a compound. That would make the results more presentable and easy to understand.***


