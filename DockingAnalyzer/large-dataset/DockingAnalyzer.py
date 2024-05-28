
#!/usr/bin/env python3

from __future__ import print_function
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import os
import os.path
import glob
import sys, fnmatch
import pymol
from pymol import cmd
import numpy as np
import center_of_mass
import math

'''
Author: Dr. Muniba Faiza
Copyright Muniba Faiza 2024
License GPL-2.0

'''

'''
This Python script identifies whether a ligand is binding within a binding pocket or around a reference ligand in the protein or somewhere else.
It is quite useful in case of high throughput screening where we dock millions of compounds.

USAGE:

python3 DockingAnalyzer.py <receptor_filename> <reference_ligand_filename>

'''

def display_info():
    banner = """
    
        ============================================================

        
        \ \ / // __| ___   /_\   _ _   __ _ | | _  _  ___(_) ___
         \ V / \__ \|___| / _ \ | ' \ / _` || || || |(_-<| |(_-<
          \_/  |___/     /_/ \_\|_||_|\__,_||_| \_, |/__/|_|/__/
                                                |__/                    

          Python package for Virtual Screening Results Analysis
"""
    info = """
        ##############################################################
        #                                                            #
        #                    DockingAnalyzer.py                      #
        #                                                            #
        ##############################################################
        # This script is designed to process a large number of       #
        # docking output files, calculating the center of mass       #
        # (COM) for each ligand pose and comparing it to the COM     #
        # of a reference ligand to determine proximity. Ligands      #
        # that are near the reference ligand's COM are flagged.      #
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

    ################################################################
    # How to cite:                                                 #
    #                                                              #
    # 1. Faiza, M., (2024). dockinganalyzer-py: a-new-python-      #
    # script-to-identify-ligand-binding-in-protein-pockets,        #
    # 10(5): page 12-16. https://bioinformaticsreview.com/20240110 #
    # /vs_analysis-a-python-package-to-perform-post-virtual-       #
    # screening-analysis/                                          #
    #                                                              #
    # 2. Faiza, M., (2024). VS_Analysis: A Python package to       #
    # perform post-virtual screening analysis, 10(1): page 8-12.   #
    # https://bioinformaticsreview.com/20240110/vs_analysis-a-     #
    # python-package-to-perform-post-virtual-screening-analysis/   #
    ################################################################


"""
	print(cite_info)
	

# Function to calculate center of mass of docked ligands
def calculate_COM(poses_names, vina_docking_file, ref_ligand_com, threshold):
    with open("hts-output-analysis.txt", "a") as outfile:
        for pose in poses_names:

            # Define selections for the current pose
            ligand_selection = f"'{pose}'"
            ref_com = ref_ligand_com
            
            # Select the current pose
            cmd.select('ligand_selecn', ligand_selection)

            # Calculate center of mass of the current pose
            com = cmd.centerofmass(selection='ligand_selecn')

            # Round off each coordinate to 3 decimal places
            com_rounded = [round(coord, 3) for coord in com]

            # Round off reference ligand center of mass to 3 decimal places
            ref_com_rounded = [round(coord, 3) for coord in ref_com]
            
            # Calculate the magnitude of the difference vector
            difference_vector = np.array(com) - np.array(ref_ligand_com)
            difference_magnitude = np.linalg.norm(difference_vector)

            # Round off the difference magnitude to 3 decimal places
            difference_magnitude_rounded = round(difference_magnitude, 3)
            
            # Check if the magnitude is below the threshold
            if difference_magnitude < threshold:
                is_near_ref_ligand = "Yes"

                with open("near_ligand.txt", "a") as near_ligand_file:

                    # Write the names of vina output files and poses that are near the reference ligand to the separate file
                    near_ligand_file.write(f"{vina_docking_file}\t{pose}\t{difference_magnitude_rounded}\n")
            else:
                is_near_ref_ligand = "No"
            
            # Write information to output file
            outfile.write(f"{vina_docking_file}\t{pose}\t{com_rounded}\t{difference_magnitude_rounded}\t{is_near_ref_ligand}\n")

        # Write a separator line after processing each file
        outfile.write("\n" + "-"*40 + "\n\n")


# Function to process Vina output files
def process_files(file_list, mypath, ref_ligand_name, ref_ligand_com):
    for vinaoutfile in file_list:
        if vinaoutfile.endswith('.pdbqt'):
            vina_file_path = os.path.join(mypath+"/"+vinaoutfile)
            
            # Load Vina output file in PyMOL
            cmd.load(vina_file_path)

            print("Loading "+vina_file_path+".........\n")

            vinaoutfile_name = os.path.splitext(os.path.basename(vinaoutfile))[0]

            # Split poses of the Vina output file
            cmd.split_states(vinaoutfile_name, prefix="pose_")

            # Get the names of poses
            pose_names = cmd.get_names()[1:]

            # Calculate center of mass and difference for each pose
            calculate_COM(pose_names, vinaoutfile_name, ref_ligand_com, threshold=4.0) # Adjust the threshold here

            # Delete all objects to free memory
            cmd.delete('*')

    # Delete the loaded receptor and reference ligand structures
    cmd.delete('receptor')
    cmd.delete('reference_ligand')
    cmd.delete('vinaoutfile')


def main():

    display_info()
    
    receptor_file = sys.argv[1]
    reference_ligand = sys.argv[2]
    reference_ligand_name = os.path.splitext(os.path.basename(reference_ligand))[0]

    # Get path of current directory
    mypath = os.path.abspath(os.getcwd())
    
    # Read all filenames in the directory
    file_list = os.listdir(mypath)
    
    # Collecting the total number of Vina output files in the directory
    num_files = len(fnmatch.filter(file_list, '*.pdbqt'))
    print('There are',num_files, 'vina output files in the current directory\n\n')

    receptor_path = os.path.join(mypath+"/"+receptor_file)
    ref_lig_path = os.path.join(mypath+"/"+reference_ligand)

    # Load receptor file in PyMOL
    pymol.finish_launching()
    cmd.load(receptor_path)
    print('\nLoading receptor: ',receptor_file,'...........\n')

    # Load reference ligand in PyMOL
    cmd.load(ref_lig_path)
    print('\nLoading reference ligand: ',reference_ligand,'...........\n')

    # Calculate center of mass of the reference ligand
    ref_ligand_com = cmd.centerofmass(selection=f"'{reference_ligand_name}'")
    ref_ligand_com_rounded = [round(coord, 3) for coord in ref_ligand_com]                      # rounding off upto 3 digits.

    # Delete all objects to free memory
    cmd.delete('*')

    # Write reference ligand COM to the output file
    with open("hts-output-analysis.txt", "a") as outfile:

        # Write reference ligand COM to the output file
        outfile.write(f"Reference Ligand COM: {ref_ligand_com_rounded}\n\n\n")

        # Write column names to the output file
        outfile.write("Ligand name\tPose name\tCOM\tDifference COM\tIs near Reference Ligand?\n\n")

    if num_files <= 100:
        process_files(file_list, mypath, reference_ligand_name, ref_ligand_com_rounded)
    else:
        batch_size = 100
        num_batches = math.ceil(num_files / batch_size)
        print(f'.......There are {num_batches} batches.......\n\n')
        
        for i in range(num_batches):
            print(f"\n\n******* Processing batch {i + 1}/{num_batches} *********\n\n")
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, num_files)
            batch_files = file_list[start_index:end_index]
            print("Batch files:", batch_files, "\n")  # Print batch files
            process_files(batch_files, mypath, reference_ligand_name, ref_ligand_com_rounded)

    # Close PyMOL
    pymol.cmd.quit()

    print("All files have been processed!\n\n")
    cite_info()


# Run the main function
if __name__ == "__main__":
    main()


