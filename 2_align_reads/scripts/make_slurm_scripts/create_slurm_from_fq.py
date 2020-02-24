#!/usr/bin/env python3

# Script to create slurm array job files from svsim mock genome (.fa) files. random_reads_template.txt should be in same directory.

# python3 create_slurm_from_fq.py /work/Wasmuth_lab/mrkyle/repos/sv_pipeline/0_create_training_data/bbtools/random_reads_output/deletions 
import fileinput
import argparse
import os

TEMPLATE_FILE="./random_reads_template.txt"

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Parent directory for the simulated genomes (.fa format).")
parser.add_argument("output_dir", help="Directory to export the slurm files to")
args = parser.parse_args()

depth = 2 # Script is intended to be used with subdirectories one directory deep in parent folder
if os.path.isdir(args.input_dir):
	array_index=1
	my_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.input_dir)))
	for root,dirs,files in os.walk(my_dir):
		if root[len(my_dir):].count(os.sep) < depth:
			for f in files:
				if f.endswith("1.fq"):
					create_template_replacements(root, f,array_index)
					array_index+=1
