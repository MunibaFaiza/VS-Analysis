# Author: Dr. Muniba Faiza
# Copyright Muniba Faiza 2022
# License GPL-2.0


#!/usr/bin/env python3

import os
import os.path
import glob
import itertools
import collections
import pprint
import sys
import fnmatch


#get path of current dir

mypath = os.getcwd()

print ("\nDirectory path detected \n")


#get compound name

comp_name = sys.argv[1]


#read all filenames in the dir

file_list = os.listdir(mypath)


#collecting the total number of log files in the directory.

num_files = len(glob.glob1(mypath,"*log*.txt"))
print('There are',num_files, 'log files in the current directory\n\n')


#looking for Binding affinity

for file_name in file_list:


	if fnmatch.fnmatch(file_name, '*'+comp_name+'*.txt'):
		with open(os.path.join(mypath, file_name), "r") as src_file:
						
			for line in src_file:
				try:
					if '-+' in line:													#looking for binding affinity table
						nextline = next(src_file)
						value = nextline[nextline.find("-")+0:].split()[0]					#split at '-' and print binding affinity including '-'
						
				except IndexError:
					continue

print("The Binding Affinity of "+comp_name+" is : "+value+"\n")