'''
Author: Dr. Muniba Faiza
Copyright Muniba Faiza 2021
License GPL-2.0

'''



#!/usr/bin/env python3

import os
import os.path
import glob
import itertools
import collections
import pprint
import sys


#get path of current dir

mypath = os.path.abspath(os.getcwd())

print ("Directory path detected \n")



#read all filenames in the dir

file_list = os.listdir(mypath)



#collecting the total number of log files in the directory.

num_files = len(glob.glob1(mypath,"*log*.txt"))
print('There are',num_files, 'log files in the current directory\n\n')



# Create an empty dict

file_dict = {}

for file_name in file_list:

	import fnmatch
	if fnmatch.fnmatch(file_name, '*log*.txt'):
		with open(os.path.join(mypath, file_name), "r") as src_file:
			
			
			for line in src_file:
				try:
					if '-+' in line:													#looking for binding affinity table
						nextline = next(src_file)
						value = nextline[nextline.find("-")+0:].split()[0]					#split at '-' and print binding affinity including '-'
						file_dict[file_name] = value
				except IndexError:
					continue
				
from collections import OrderedDict
from operator import itemgetter



#sorting binding affinities

sorted_dict = OrderedDict(sorted(file_dict.items(), key=itemgetter(1), reverse=True))
print ("Binding affinities sorted \n\n")



#function for sorting binding affinities based on a cutoff

def ba_cutoff():
	cutoff = eval(input("Enter the cut off value:\n"))												#getting cutoff value from user

	for line in sorted (sorted_dict.values()) :
		
		if(float(line)>=float(cutoff)):																#looking for binding affinities >= user inputted cutoff value
			with open("ba_output.txt", "w") as outfile:
				print("Your cutoff value =", cutoff, "\n", file=outfile)
				print('\n'.join("{}: {}".format(k, v) for k, v in sorted_dict.items()), file=outfile)					#getting filenames and corresponding binding affinities in a file
				sys.exit ("Done! The result is provided in the 'ba_output.txt' file.")
	else:
		sys.exit("No compounds were found with the provided binding affinity value.")



#asking user whether he wants to sort binding affinities based on a cutoff value.

query = input("Would you like to sort files based on binding affinity? [yes|no]\n")
if query.lower() in ["n","no"]:
	pass 
	print("Continuing with general sorting.\n")
elif query.lower() in ["y","yes"]:
	ba_cutoff()
else:
	sys.exit("Please enter (yes/no) or (y/n) \n")


n = eval(input("Enter the number of compounds for which you want to get binding affinities:\n"))


#checking if the user input is correct.

if n>num_files:
	print('Enter a valid number. The number you entered exceeds the total number of log files present in the current directory.\n\n')
	sys.exit()

with open("output.txt", "w") as f:
	
	firstnpairs = list(sorted_dict.items())[:n]							                                    #get first n elements from dict

	print('\n'.join("{}: {}".format(k, v) for k, v in firstnpairs), file=f)			                        #print results without quotes

print ("Done! The result is provided in the 'output.txt' file.")
				
