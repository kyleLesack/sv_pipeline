#!/usr/bin/python3
# Script for converting SVSIM .bedpe files into VCF format compatible with Structural Variation Engine
# Kyle Lesack
# 2020-01-29
# Requires VCF_Header.txt in same working directory that Python is invoked from
# NOTE: The reported SV length and coordinates vary between sv callers in SVE
# E.g. In Tigra, SV_LEN = end_coordinate - start_coordinate 
# E.g. In cnmops, SV_LEN = end_coordinate - start_coordinate + 1


import argparse
import csv
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input BED file (xxx.bedpe)")
parser.add_argument("sample", help="sample name, usually xxx part of xxx.event")

args = parser.parse_args()

date = datetime.datetime.now()
today_is_the_greatest = (str(date.year) + "-" + str(date.month) + "-" + str(date.day))

# Read VCF Header file
with open('VCF_Header.txt', 'r') as header_file :
	header_data = header_file.read()
	
# Replace the target string
header_data = header_data.replace('DATE', today_is_the_greatest) # Write the correct date in vcf header

REF_ALLELE = "N" # VCF files have a reference allele field, I don't think that SVE needs this. I don't want to find it in the FASTA file.
VARIANT_QUAL = "." # Simulated data, so a "." (unknown quality) is used
VARIANT_FILTER = "PASS" # Simulated data, so PASS is used for filter field
sample_name = args.sample


print(header_data, end='')

## Example row from svsim bedpe file
# X       4784522 4784523 X       4784623 4784624 DEL05::X::54    255     +       +

## Example row from svsim event file
#DEL05   DEL     100     X       4784523 X       4784523 +       X       4784622 + 

## Example vcf file header and record
#CHROM        POS     ID      REF     ALT     QUAL    FILTER  INFO
#IV      17439809        SVSIM_DEL01_100bp       N       <DEL>   .       PASS    DBVARID;CALLID=SVSIM_DEL01_100bp;SVTYPE=DEL;EXPERIMENT=1;SAMPLE=SVSIM_DEL-100-1000bp;END=17439908;REGION=NA

with open(args.input) as fd:
	rd = csv.reader(fd, delimiter="\t", quotechar='"')
	for row in rd:
		chromosome = row[0]
		start_coord = row[2]
		end_coord = row[4]
		sv_length = int(end_coord) - int(start_coord)
		variant_type = row[6][0:3]
		call_id = row[6][0:5]
		variant_id = "SVSIM_" + call_id + "_" + str(sv_length) + "bp"
		alt_allele = "<" + variant_type + ">" # ALT field is used to store the variant type in the VCF file
		variant_info = "DBVARID;" + "CALLID=" + variant_id + ";" + "SVTYPE=" + variant_type + ";" + "EXPERIMENT=1;" + "SAMPLE=" + sample_name + ";" + "END=" + end_coord + ";" + "REGION=NA"
		#print(variant_info)		
		vcf_row = chromosome + "\t" + start_coord + "\t" + variant_id + "\t" + REF_ALLELE + "\t" + alt_allele + "\t" + VARIANT_QUAL + "\t" + VARIANT_FILTER + "\t" + variant_info
		print(vcf_row)
