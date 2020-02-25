#!/usr/bin/env python3

# Script to create slurm array job files from SVE vcf files. fusorsv_template.txt should be in same directory.

# python3 create_slurm_from_s0_vcf.py /work/Wasmuth_lab/mrkyle/repos/sv_pipeline/3_call_svs/output/deletions/ deletions
import fileinput
import argparse
import os

TEMPLATE_FILE="./fusorsv_template.txt"

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Parent directory for the alignment files (.bam format).")
parser.add_argument("output_dir", help="Directory to export the slurm files to")
args = parser.parse_args()

def create_slurm_script(input_dir, output_dir,file_prefix,array_index):
	with open(TEMPLATE_FILE, 'r') as file :
		output_file = args.output_dir +"/" + file_prefix + "." + str(array_index)
		filedata = file.read()
		filedata = filedata.replace('INPUT_DIR', input_dir)
		filedata = filedata.replace('OUTPUT_DIR', output_dir)


		with open(output_file, 'w') as file:
			file.write(filedata)
	

# Function determines the variable values that will replace the dummy placeholders in the template file
def create_template_replacements(root, f,array_index):
	input_dir = root + "/"
	output_dir = input_dir.replace("3_call_svs","4_fusorsv")
#	file_prefix=f.split("_S0.vcf")[0]
	file_prefix=f.strip("_S0.vcf")
	create_slurm_script(input_dir,output_dir,file_prefix,array_index)


depth = 2 # Script is intended to be used with subdirectories one directory deep in parent folder
if os.path.isdir(args.input_dir):
	array_index=1
	my_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.input_dir)))
	for root,dirs,files in os.walk(my_dir):
		if root[len(my_dir):].count(os.sep) < depth:
			for f in files:
				if f.endswith("S0.vcf"): # Looks for truth file in directory
					create_template_replacements(root, f,array_index)
					array_index+=1
				



