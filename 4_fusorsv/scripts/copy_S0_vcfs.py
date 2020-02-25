#!/usr/bin/env python3
# Helper script that prints to screen the commands to copy FusorSV truth vcf files to folders containing SVE variant calls

# python3 copy_S0_vcfs.py input_dir 
import fileinput
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Parent directory with subdirectories for each vcf file to be copied to the call_svs output directory.")
args = parser.parse_args()

def copy_s0_file(root,input_file):
	output_dir = root.replace('0_create_training_data/svsim/', "3_call_svs/")
	print("cp " + input_file + " " + output_dir + "/")


depth=2

if os.path.isdir(args.input_dir):
	my_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.input_dir)))
	for root,dirs,files in os.walk(my_dir):
		if root[len(my_dir):].count(os.sep) < depth:
			for f in files:
				if f.endswith("S0.vcf"):
					input_file= os.path.join(root,f)
					copy_s0_file(root,input_file)

