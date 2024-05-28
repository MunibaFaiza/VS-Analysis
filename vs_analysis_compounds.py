'''
Author: Dr. Muniba Faiza
Copyright Muniba Faiza 2022
License GPL-2.0

'''

'''
This script allows users to search for specific binding affinities corresponding to compound names.

'''

#!/usr/bin/env python3

import os
import os.path
import glob
import itertools
import collections
import pprint
import sys
import fnmatch


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
		#                 vs_analysis_compounsd.py                   #
		#                                                            #
		##############################################################
		#                                                            #
		# This script allows users to search for specific binding    #
		# affinities corresponding to compound names. Users must     #
		# provide a compound name as an argument given that the      #
		# same compound name is present in the log filenames.        #
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
    # 1. Faiza M., (2022). vs_analysis_compound.py: Python       #
    # script to search for binding affinities based on compound  #
    # names. 8(9):page 8-12. The article is available at         #
    # https://bioinformaticsreview.com/20220917/vs_analysis_     #
    # compound-py-python-script-to-search-for-binding-affinities #
    # -based-on-compound-names/                                  #
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

cite_info()