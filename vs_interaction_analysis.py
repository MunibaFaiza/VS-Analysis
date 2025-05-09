'''
Author: Dr. Muniba Faiza
Copyright Muniba Faiza 2024
License GPL-2.0

'''


#!/usr/bin/env python3

from __future__ import print_function
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI


import sys, os, glob, fnmatch
import pymol
from pymol import cmd, stored
import re
from get_raw_distances import get_raw_distances


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
		# This script allows users to calculate the number of        #
		# hydrogen bonds and their distances for each pose. This     #
		# script also provides names of the amino acid residues      #
		# close to the docked ligand.                                #
		#                                                            #
		##############################################################


    """
    print(banner)
    print(info)


def cite_info():

	cite_info= """

    ##################################################################
    # How to cite:                                                   #
    # 1. Faiza M., (2024). vs_interaction_analysis.py: Python script #
    # to perform post-virtual screening analysis. 10(1):page 4-8.    #
    # The article is available at                                    #
    # https://bioinformaticsreview.com/20240110/vs_interaction_      #
    # analysis-py-python-script-to-perform-post-virtual-screening    #
    # -analysis/                                                     #
    # 2. Faiza, M., (2024). VS_Analysis: A Python package to perform #
    # post-virtual screening analysis, 10(1): page 8-12.             #
    # https://bioinformaticsreview.com/20240110/vs_analysis-a-       #
    # python-package-to-perform-post-virtual-screening-analysis/     #
    ##################################################################

"""
	print(cite_info)
     
    
display_info()

#get path of current dir

mypath = os.path.abspath(os.getcwd())

print ("Directory path detected \n")

#read all filenames in the dir

file_list = os.listdir(mypath)


#collecting the total number of vina output files in the directory.

num_files = len(glob.glob1(mypath,"*.pdbqt"))
print('There are',num_files, 'vina output files in the current directory\n\n')


#get the name of the receptor file
receptor = input("Enter the receptor filename: \n")

receptor_name = os.path.splitext(os.path.basename(receptor))[0]

receptor_path= os.path.join(mypath+"/"+receptor)

outfile = open("num-hbonds.txt", "a")

# Function to calculate the number of H-bonds and their distances for each pose
def calculate_hbonds(poses_names, vina_docking_file):

    print(f"\n\nProcessing Vina file name: {vina_docking_file}\n")
    
    # Write the processing message to the output file
    outfile.write(f"\n\nProcessing Vina file name: {vina_docking_file}\n\n")

    for pose in poses_names:
            
            bonds="hbonds"
            bonds = cmd.get_legal_name(bonds)

            # If the group of contacts already exists, delete them
            cmd.delete(bonds)


            # Define selections for the current pose
            receptor_selection = f"'{receptor_name}' and (donors | acceptors)"
            ligand_selection = f"'{pose}' and (donors | acceptors)"

            
            # Select the current pose
            cmd.select('receptor_selecn', receptor_selection)
            cmd.select('ligand_selecn', ligand_selection)
            

            # Compute possibly suboptimal polar interactions using the bigcutoff = 4.0 and radius = 3.5
            # These are the default values. Adjust them according to your requirements.

            pol_res = bonds+"_polar"                    
        
            cmd.distance(pol_res, 'receptor_selecn', 'ligand_selecn', 4.0, mode = 1) 
            cmd.set("dash_radius", "0.06", pol_res)
            
            cmd.distance("hbonds", 'receptor_selecn', 'ligand_selecn', 3.5, mode=2)
            
            D = get_raw_distances("hbonds")

            output = f"Number of Suboptimaml Polar Hbonds for {pose}: {len(D)}\n"
            print(output)
            outfile.write(output)

            # Print distances for each H-bond
            for item in D:
                distance_value = round(item[2], 2)
                distance_output = f"Distance: {distance_value}\n"
                print(distance_output)
                outfile.write(distance_output)

            # Add a newline to separate the information for the next pose
            print()
            outfile.write("\n")

# Function to find the residue names around the ligand within a specified distance of 3.2 Angstroms.
def res_around_ligand(protein_file, ligand_file, pose_name, vina_output_file):

    for pose in pose_name:

        result = "contacts"
        result = cmd.get_legal_name(result)

        contacts="contactsfull"
        contacts = cmd.get_legal_name(contacts)

        #if the group of contacts already exist, delete them
        cmd.delete(result)
        cmd.delete(contacts)

        # Select the current pose
        cmd.frame(int(pose.split('_')[-1]))

        # Select atoms around 3.2 angstroms from the Vina output file. You can change the distance in the following command.
        cmd.select("contacts", f"'{vina_output_file}' around 3.2")

        # Select contactsfull by residues
        cmd.select("contactsfull", "byres contacts")

        # Show sticks for contactsfull
        cmd.show("sticks", "contactsfull")

        # Use PyMOL's cmd.iterate to collect the names of contact residues
        stored.contact_list = []
        cmd.iterate("(contactsfull) and name ca", 'stored.contact_list.append((chain, resi, resn))')

        # Print the contact residues in the terminal
        print("Protein filename: {}".format(protein_file))
        print("Ligand docked filename: {}".format(ligand_file))
        print("Pose name: {}".format(pose))
        print("Contact residues:")
        for residue_info in stored.contact_list:
            print("{} {} {}".format(residue_info[0], residue_info[1], residue_info[2]))

        # Save information to the output file
        with open("residues.txt", "a") as output_file:
            output_file.write("Protein filename: {}\n".format(protein_file))
            output_file.write("Ligand docked filename: {}\n".format(ligand_file))
            output_file.write("Pose name: {}\n".format(pose))

            # Write each residue information in a new line
            for residue_info in stored.contact_list:
                output_file.write("{} {} {}\n".format(residue_info[0], residue_info[1], residue_info[2]))

            # Add a separator between poses
            output_file.write("\n")


for vinaoutfile in file_list:

    if fnmatch.fnmatch(vinaoutfile, '*.pdbqt'):

        vina_file_path = os.path.join(mypath+"/"+vinaoutfile)
        #print(vina_file_path)
           

        # Load receptor file in Pymol
        pymol.finish_launching()
        pymol.cmd.load(receptor_path)
        print('\nLoading receptor: ',receptor,'...........\n')
                    
                
        # Load Vina output file in Pymol
        pymol.cmd.load(vina_file_path)
        vinaoutfile_name = os.path.splitext(os.path.basename(vinaoutfile))[0]

        # Split poses of the vina output file
        cmd.split_states(vinaoutfile_name, prefix="pose_")

        # Get the total number of poses
        num_states = cmd.count_states()

        # Get the names of poses
        title = cmd.get_names()

        pose_names = title[2:]              # excluding the protein & ligand name from the list (i.e., title)

        # Call the function to calculate the H-bonds and their distances.
        calculate_hbonds(pose_names, vinaoutfile)

        # Identify the amino acid residues around the ligand.
        res_around_ligand(receptor, vinaoutfile, pose_names, vinaoutfile_name)

    cmd.reinitialize('everything')

# Close the file when done writing
outfile.close()

cite_info()
