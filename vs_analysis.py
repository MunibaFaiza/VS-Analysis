'''
Author: Dr. Muniba Faiza
Copyright Muniba Faiza 2021
License GPL-2.0

'''

'''
This Python script identifies top poses with the lowest binding affnities from the Vina output log files in a directory.

USAGE:

python3 vs_analysis.py

'''


#!/usr/bin/env python3

import os
import os.path
import glob
import itertools
import collections
import pprint
import sys


def display_info():
    banner = """
    
        ============================================================

        
        \ \ / // __| ___   /_\   _ _   __ _ | | _  _  ___(_) ___
         \ V / \__ \|___| / _ \ | ' \ / _` || || || |(_-<| |(_-<
          \_/  |___/     /_/ \_\|_||_|\__,_||_| \_, |/__/|_|/__/
                                                |__/                    

           Python package for Virtual Screening Result Analysis
"""
    info = """
        ##############################################################
		#                                                            #
		#                    vs_analysis.py                          #
		#                                                            #
		##############################################################
		# This script identifies top poses with the lowest binding   #
		# affinities from log files in a directory. It retrieves a   #
		# user-specified number of compounds based on their top pose #
		# binding affinities. Additionally, users can set a binding  #
		# affinity threshold to filter and list compounds exceeding  #
		# this value. The output file includes filenames and their   #
		# corresponding binding affinities, sorted in ascending      #
		# order.                                                     #
		#                                                            #
		# Author: Dr. Muniba Faiza                                   #
		# Bioinformatics Review                                      #
		#                                                            #
		##############################################################

    """
    print(banner)
    print(info)


def cite_info():

	cite_info= """

    ##############################################################
    # HOW TO CITE:                                               #
    #                                                            #
    # 1. Faiza M., (2021). vs_Analysis.py: A Python Script to    #
    # Analyze Virtual Screening Results of Autodock Vina 8(5):   #
    # page 12-16. The article is available at                    #
    # https://bioinformaticsreview.com/20210509/vs-analysis-a-   #
    # python-script-to-analyze-virtual-screening-results-of-     #
    # autodock-vina/                                             #
    #                                                            #
    # 2. Faiza, M., (2024). VS_Analysis: A Python package to       #
    # perform post-virtual screening analysis, 10(1): page 8-12. #
    # https://bioinformaticsreview.com/20240110/vs_analysis-a-   #
    # python-package-to-perform-post-virtual-screening-analysis/ #
    ##############################################################

"""
	print(cite_info)
	

display_info()

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
				
cite_info()