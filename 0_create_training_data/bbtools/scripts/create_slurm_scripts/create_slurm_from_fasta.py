#!/usr/bin/env python3

# Script to create slurm array job files from svsim mock genome (.fa) files. random_reads_template.txt should be in same directory.

# python3 create_slurm_from_fasta.py ../../../svsim/output/deletions/ ./deletions
import fileinput
import argparse
import os

TEMPLATE_FILE="./random_reads_template.txt"

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Parent directory for the simulated genomes (.fa format).")
parser.add_argument("output_dir", help="Directory to export the slurm files to")
parser.add_argument('--error', action='store_true', dest='error_model', help='Random reads will simulate sequencing errors.')
args = parser.parse_args()


def create_slurm_script(job_prefix,reference_fasta_file,random_reads_path,error_model,array_index):
	with open(TEMPLATE_FILE, 'r') as file :
		output_file = args.output_dir +"/" + job_prefix + "." + str(array_index)
		filedata = file.read()
		filedata = filedata.replace('REFERENCE_FILE', reference_fasta_file)
		filedata = filedata.replace('OUTPUT_DIR', random_reads_path)
		filedata = filedata.replace('FILE_PREFIX', job_prefix)
		filedata = filedata.replace('ERROR_MODEL', error_model)

		with open(output_file, 'w') as file:
			file.write(filedata)
	

# Function determines the variable values that will replace the dummy placeholders in the template file
def create_template_replacements(root, f,array_index):
	random_reads_path = root.replace("svsim", "bbtools")
	if args.error_model:
		random_reads_path = random_reads_path.replace("output", "random_reads_output_with_errors")
		error_model="t"
	else:
		random_reads_path = random_reads_path.replace("output", "random_reads_output")
		error_model="f"
	reference_fasta_file = os.path.join(root,f) # NOTE: The reference file is the mock genome .fa file generated by svsim, not the C. elegans reference genome
	job_prefix=f.split(".fa")[0]
	create_slurm_script(job_prefix,reference_fasta_file,random_reads_path, error_model,array_index)


depth = 2 # Script is intended to be used with subdirectories one directory deep in parent folder
if os.path.isdir(args.input_dir):
	array_index=1
	my_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.input_dir)))
	for root,dirs,files in os.walk(my_dir):
		if root[len(my_dir):].count(os.sep) < depth:
			for f in files:
				if f.endswith(".fa"):
					create_template_replacements(root, f,array_index)
					array_index+=1



