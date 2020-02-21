#!/usr/bin/env python3


# python3 svsim2vcf.py input_file sample_name
import fileinput
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Parent directory with subdirectories for each bedpe file to be converted to vcf.")
args = parser.parse_args()

def print_svsim2vcf_commands(sample_name, input_file,output_dir):
	outfile=output_dir + "/" + sample_name + "_S0.vcf"
	print("python3 svsim2vcf.py " + str(input_file) + " " + sample_name + "  > " + outfile )

depth=2

if os.path.isdir(args.input_dir):
	my_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.input_dir)))
	for root,dirs,files in os.walk(my_dir):
		if root[len(my_dir):].count(os.sep) < depth:
			for f in files:
				if f.endswith(".bedpe"):
					sample_name= f.strip(".bedpe")
					input_file= os.path.join(root,f)
					print_svsim2vcf_commands(sample_name, input_file, root)
