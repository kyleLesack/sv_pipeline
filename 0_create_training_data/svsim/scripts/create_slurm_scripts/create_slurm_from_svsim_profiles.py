#!/usr/bin/env python3

# python3 create_slurm_from_svsim_profiles.py ~/my_projects/repos/sv_pipeline/0_create_training_data/svsim/profiles/deletions/
import fileinput
import argparse
import os

OUTPUT_DIR_PREFIX="/work/Wasmuth_lab/mrkyle/repos/sv_pipeline/0_create_training_data/svsim/output/"
REFERENCE_FILE="/home/kyle.lesack1/project_files/reference_genome/c_elegans.PRJNA13758.WS263.genomic.fa"

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Directory containing the svsim profile files. Requires .txt extension.")
parser.add_argument("output_dir", help="Directory to export the slurm files to")
parser.add_argument("sv_type", help="Variant type. Must be DEL, DUP, INS, or INV")
args = parser.parse_args()

def make_slurm_file(profile_file,job_name,array_id_number,template_file):
	with open(template_file, 'r') as file :
		filedata = file.read()
		filedata = filedata.replace('REFERENCE_FILE', REFERENCE_FILE)
		filedata = filedata.replace('PROFILE_FILE', profile_file)
		filedata = filedata.replace('JOBNAME', job_name)
		filedata = filedata.replace('OUTPUT_DIR', output_dir)
		output_file=job_name+ "." + str(array_id_number)
		output_file=args.output_dir + "/" + output_file
		with open(output_file, 'w') as file:
			file.write(filedata)


		
def get_profile_files(template_file):
	array_id_number = 1 # each job in a slurm array is assigned a number; slurm array submission script will call svsim sh scripts using this number 
	for file in os.listdir(args.input_dir):
		if file.endswith(".txt"):
			profile_file= args.input_dir + file
			base=os.path.basename(file)
			job_name = os.path.splitext(base)[0] # Job name is based on the the profile file name, excluding the extension
			make_slurm_file(profile_file,job_name,array_id_number,template_file)
			array_id_number += 1



if args.sv_type=="DEL":
	output_dir=OUTPUT_DIR_PREFIX + "deletions/"
	template_file = "./DEL_template.txt"
	if os.path.isdir(args.output_dir):
		get_profile_files(template_file)
	else:
		print("output path not found")

elif args.sv_type=="DUP":
	output_dir=OUTPUT_DIR_PREFIX + "duplications/"
	template_file = "./DUP_template.txt"

	if os.path.isdir(args.output_dir):
		get_profile_files(template_file)
	else:
		print("output path not found")

elif args.sv_type=="INS":
	output_dir=OUTPUT_DIR_PREFIX + "insertions/"
	template_file = "./INS_template.txt"

	if os.path.isdir(args.output_dir):
		get_profile_files(template_file)
	else:
		print("output path not found")

elif args.sv_type=="INV":
	output_dir=OUTPUT_DIR_PREFIX + "inversions/"
	template_file = "./INV_template.txt"
	if os.path.isdir(args.output_dir):
		get_profile_files(template_file)
	else:
		print("output path not found")

else:
	print("Please specify the variant type (DEL, DUP, INV, or INS)")




