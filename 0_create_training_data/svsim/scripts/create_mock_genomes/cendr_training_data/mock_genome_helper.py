#!/usr/bin/python3
# Simple helper script to create svsim profile files

import os
import pandas as pd
import csv
from prettytable import PrettyTable
import numpy as np


# Note: the bin sizes were taken from the callers_tbj.xxx.tsv output from FusorSV. It has includes some extra bins compared to FusorSV/fusorsv/data/bin_map.json from the FusorSV source code
DUPLICATION_BINS = ((1,50),(50,1000),(1000,10000),(10000,50000),(50000,100000),(100000,250000),(250000,500000),(500000,1000000))
DUPLICATION_BIN_HEADER = ["1-50","50-1K","1K-10K","10K-50K","50K-100K","100K-250K","250K-500K","500K-1M"]
DUPLICATION_BIN_FILENAME_SIZES = ["Small","Small","Medium","Medium","Large","Large","Large","Large"] # My files are named by grouping bins into size ranges (small, medium, and large). Used in pretty tables
duplication_bin_events =  [0] * len(DUPLICATION_BINS) # Create new list for number of duplications of each size bin
duplication_bin_bases = [0] * len(DUPLICATION_BINS) # Create new list for total number of base pairs for all events in each bin
duplication_df = pd.DataFrame({'Count': duplication_bin_events,'BP':duplication_bin_bases},index=pd.IntervalIndex.from_tuples(DUPLICATION_BINS, closed = 'left'))


DELETION_BINS=((1,50),(50,100),(100,400),(400,600),(600,950),(950,1200),(1200,1500),(1500,1900),(1900,2200),(2200,2900),(2900,3600),(3600,4800),(4800,6100),(6100,9000),(9000,18500),(18500,100000),(100000,1000000))
DELETION_BIN_HEADER = ["1-50","50-100","100-400","400-600","600-950","950-1200","1200-1500","1500-1900","1900-2200","2200-2900","2900-3600","3600-4800","4.8K-6.1K","6.1K-9K","9K-18.5K","18.5K-100K","100K-1M"]
DELETION_BIN_FILENAME_SIZES = ["Small","Small","Small","Small","Small","Medium","Medium","Medium","Medium","Medium","Medium","Medium","Medium","Medium","Medium","Large","Large"]
deletion_bin_events =  [0] * len(DELETION_BINS) # Create new list for number of deletions of each size bin
deletion_bin_bases = [0] * len(DELETION_BINS) # Create new list for total number of base pairs for all events in each bin
deletion_df = pd.DataFrame({'Count': deletion_bin_events,'BP':deletion_bin_bases},index=pd.IntervalIndex.from_tuples(DELETION_BINS, closed = 'left'))

INVERSION_BINS = ((1,50),(50,2500),(2500,3500),(3500,45000),(45000,80000),(80000,115000),(115000,180000),(180000,260000),(260000,300000),(300000,375000),(375000,500000),(500000,1000000))
INVERSION_BIN_HEADER = ["1-50","50-2500","2500-3500","3500-45K","45K-80K","80K-115K","115K-180K","180K-260K","260K-300K","300K-375K","375K-500K","500K-1M"]
INVERSION_BIN_FILENAME_SIZES = ["Small","Small","Medium","Medium","Large","Large","Large","Large","Large","Large","Large","Large"]
inversion_bin_events =  [0] * len(INVERSION_BINS) # Create new list for number of inversions of each size bin
inversion_bin_bases = [0] * len(INVERSION_BINS) # Create new list for total number of base pairs for all events in each bin
inversion_df = pd.DataFrame({'Count': inversion_bin_events,'BP':inversion_bin_bases},index=pd.IntervalIndex.from_tuples(INVERSION_BINS, closed = 'left'))

profile_file_lines = []
total_bases_in_deletions = 0
total_bases_in_duplications = 0
total_bases_in_inversions = 0

total_deletions = 0
total_duplications = 0
total_inversions = 0

GENOME_SIZE= 100286401 # C. elegans genome size

MENU = "S: Print mock genome statistics\nD: Add deletion(s) to mock genome\nU: Add duplication(s) to mock genome\nI: Add inversion(s) to mock genome\nW: Write svsim profile to disk\nB: Summarize bin membership for all profile files\nC: Create csv files containing the name of the profile file and bin memberships\nQ: Quit"

def print_mock_genome_stats(total_bases_in_deletions,total_bases_in_duplications,total_bases_in_inversions,total_deletions,total_duplications,total_inversions):
	os.system('clear')
	#choice = input("Print the filename size categories in table? E.g. small, medium, and large. Press Y to print.\n")
	choice = "Y" # skipping prompting user for this now	
	if choice == "Y" or choice == "y":
		print_size_categories = True
	else:
		print_size_categories = False

	os.system('clear')

	print("Mock genome structural variant statistics")
	print("-----------------------------------------")

	total_variants = total_deletions + total_duplications + total_inversions
	variant_sum = total_bases_in_deletions+total_bases_in_duplications+total_bases_in_inversions
	variant_percent =  (variant_sum / GENOME_SIZE) * 100	
	print("Total number of variants: " + str(total_variants))	
	print(f"Percentage of C. elegans genome covered by variants: {variant_percent:.2f}%\n")
	

	print("DELETIONS")
	print("---------")
	print("Total deletions: " + str(total_deletions))
	print("Base pairs covered by deletions: " + str(total_bases_in_deletions))
	del_percent =  (total_bases_in_deletions / GENOME_SIZE) * 100
	print(f"Percentage of C. elegans genome covered by deletions: {del_percent:.2f} %\n")


	deletion_bins = deletion_df['Count']
	del_table = PrettyTable()
	del_table.title = "Deletion Bin Membership"
	del_table.field_names = DELETION_BIN_HEADER
	
	if print_size_categories:
		del_table.add_row(DELETION_BIN_FILENAME_SIZES)
		del_table.hrules = True

	del_table.add_row(deletion_bins)
	print(del_table)
	print("\n")

	print("DUPLICATIONS")
	print("------------")
	print("Total duplications: " + str(total_duplications))
	print("Base pairs covered by duplications: " + str(total_bases_in_duplications))
	dup_percent =  (total_bases_in_duplications / GENOME_SIZE) * 100
	print(f"Percentage of C. elegans genome covered by duplications: {dup_percent:.2f} %\n")

	duplication_bins = duplication_df['Count']
	dup_table = PrettyTable()
	dup_table.title = "Duplication Bin Membership"
	dup_table.field_names = DUPLICATION_BIN_HEADER

	if print_size_categories:
		dup_table.add_row(DUPLICATION_BIN_FILENAME_SIZES)
		dup_table.hrules = True

	dup_table.add_row(duplication_bins)
	print(dup_table)
	print("\n")

	print("INVERSIONS")
	print("----------")
	print("Total inversions: " + str(total_inversions))
	print("Base pairs covered by inversions: " + str(total_bases_in_inversions))
	inv_percent =  (total_bases_in_inversions / GENOME_SIZE) * 100
	print(f"Percentage of C. elegans genome covered by inversions: {inv_percent:.2f}%\n")


	inversion_bins = inversion_df['Count']
	inv_table = PrettyTable()
	inv_table.title = "Inversion Bin Membership"
	inv_table.field_names = INVERSION_BIN_HEADER

	if print_size_categories:
		inv_table.add_row(INVERSION_BIN_FILENAME_SIZES)
		inv_table.hrules = True

	inv_table.add_row(inversion_bins)
	print(inv_table)
	#print("\n")

	input("Press any key to return to menu")

def summarize_new_variant(new_variant, variant_bins):

	if isinstance(new_variant, list): # check if multiple variants were created for new_variant
		variant_size_sum = sum(new_variant)
		variant_count = len(new_variant)
		variant_bins_interval = pd.IntervalIndex.from_tuples(variant_bins,closed='left')
		categorical_object = pd.cut(new_variant, variant_bins_interval)

	else:
		variant_size_sum = new_variant
		variant_count=1
		variant_bins_interval = pd.IntervalIndex.from_tuples(variant_bins,closed='left')
		new_variant_list = [new_variant]
		categorical_object = pd.cut(new_variant_list, variant_bins_interval)

	return variant_size_sum, variant_count,categorical_object

def update_dataframe(variant_df, categorical_object): # update the variant dataframe with categorical object (bin membership from the variant just added)
	new_count = variant_df['Count'] + pd.value_counts(categorical_object)
	variant_df['Count'] = new_count
	return variant_df

def get_sizes_in_range(start_size, end_size, incrementer):
	variant_sizes = []
	size = int(start_size)
	while size <= int(end_size):
		variant_sizes.append(size)
		size += int(incrementer)
	return(variant_sizes)	
		

def get_variants_from_user(variant_type,variant_bins,variant_header, variant_bin_filename_sizes):
	os.system('clear')
	#print(variant_type + " sizes:\n" + str(variant_header)) 
	var_table = PrettyTable()
	var_table.title = str(variant_type) + " Bin Membership"
	var_table.field_names = variant_header
	var_table.add_row(variant_bin_filename_sizes)

	print(var_table)
	
	print("\nTo add a single variant, specify the same starting size and ending size. Note: The first number in the bin range sizes is inclusive in that bin (e.g., deletion size 50 would go in the 50-100 binm not 1-50)")
	print("Please enter integers only")
	variant_sizes = [] # Create list to store the size of each variant to be added. Note: svsim uses a start and stop size, along with an increment, to determine the number and size of variants
	profile_file_line = [] # Line to be added to the profile file
	start_size = input("Enter the variant starting size: ")
	end_size = input("Enter the variant ending size: ")
	try:
		if int(start_size) == int(end_size):
			variant_sizes = int(start_size)
			profile_file_line = str(variant_type) + " " + str(start_size) + " " + str(end_size)			
		elif int(start_size) > int(end_size):
			print("Start size should be less than end size")
		elif int(start_size) < int(end_size):
			incrementer = input("Enter the increment size: ")
			try:			
				variant_sizes = get_sizes_in_range(start_size, end_size, incrementer)
				profile_file_line = str(variant_type) + " " + str(start_size) + " " + str(end_size) + " " + str(incrementer) 
			except ValueError:
				print("Increment size must be an integer value only")

	except ValueError:
		print("Sizes must be integer values only")


	if profile_file_line != "" and variant_sizes:
		return  profile_file_line, variant_sizes

# Write svsim profile file to disk
def write_profile_txt(profile_file_lines, profile_file):
	try:
		with open(profile_file, "w+") as outfile:
			outfile.write('\n'.join(profile_file_lines))
			print("Created new profile file: " + str(profile_file))
	except:
		print("Unable to write profile file")

# Write the new variant(s) bin memberships for deletions, duplications, and inversions to file
def write_bin_membership(deletion_df,duplication_df,inversion_df,bin_file):
	deletion_bins =  deletion_df['Count']
	duplication_bins =  duplication_df['Count'] 
	inversion_bins =  inversion_df['Count']
	try:  
		with open(bin_file,'w') as result_file:
			wr = csv.writer(result_file)
			wr.writerow(deletion_bins)
			wr.writerow(duplication_bins)
			wr.writerow(inversion_bins)
			print("Created new bin membership file: " + str(bin_file))
	except:
		print("Unable to write bin membership file")


def write_svsim_profile(deletion_df,duplication_df,inversion_df,profile_file_lines):
	reset_dataframes = False # Reset variant dataframes to empty if this is true
	working_dir = os.getcwd()
	print("Current working directory is: " + str(working_dir))
	outdir = str(working_dir) + "/" + "output/"
	print("Default directory to write svsim profile files is: " + str(outdir)) 	
	file_prefix = input("\nPlease enter the filename prefix. A txt and csv file will be written to the output directory. These contain the svsim profile file and a csv file containing the variant bin membership. \n\nEnter filename prefix: ")
	profile_file = outdir + file_prefix + ".txt"
	bin_file = outdir + file_prefix + ".csv"
	if os.path.isfile(profile_file) or os.path.isfile(bin_file)  :
		choice = input("Output file(s) already exist. Enter y to overwrite. Overwrite? ")
		if choice == "y" or choice == "Y":
			write_profile_txt(profile_file_lines, profile_file)
			write_bin_membership(deletion_df,duplication_df,inversion_df,bin_file)
			reset_dataframes = True
	else:
		write_profile_txt(profile_file_lines, profile_file)
		write_bin_membership(deletion_df,duplication_df,inversion_df,bin_file)
		reset_dataframes = True

	input("Press any key to return to menu\n")
	return reset_dataframes

# Summarizes the variant bin membership for csv files in ./output directory
# print_to_screen variable used to determine if summaries printed to screen. If False, it just updates the bin membership for write_profile_names_and_bin_membership() function
def summarize_bin_membership(print_to_screen):

	deletion_bins = deletion_bin_events # populates list with zeros with the number of bins created earlier
	duplication_bins = duplication_bin_events
	inversion_bins = inversion_bin_events

	working_dir = os.getcwd()
	csvdir = str(working_dir) + "/" + "output/"
	if os.path.isdir(csvdir):

		for path in os.listdir(csvdir):
			full_path = os.path.join(csvdir, path)
			if os.path.isfile(full_path) and path.endswith(".csv"):
				with open(full_path, newline='') as csvfile:
					bin_reader = csv.reader(csvfile, delimiter=',')
					csv_rows=[row for row in bin_reader]
					row_integers = [] # create list to store csv row elements as integers (they are read as strings with csv.reader)
					for row in csv_rows:					
						row = [int(i) for i in row]
						row_integers.append(row)
					
					csv_dels = row_integers[0] # deletion bins in csv file
					deletion_bins = np.add(deletion_bins,csv_dels)
					csv_dups = row_integers[1] # duplication bins in csv file
					duplication_bins = np.add(duplication_bins,csv_dups)
					csv_invs = row_integers[2] # inversion bins in csv file
					inversion_bins = np.add(inversion_bins,csv_invs)

	else:
		print("Requires csv files in ./output")


	if print_to_screen:
		os.system('clear')

		#choice = input("Print the filename size categories in table? E.g. small, medium, and large. Press Y to print.\n")
		choice = "Y" # Change back to user input above if I want to prompt for this
		if choice == "Y" or choice == "y":
			print_size_categories = True
		else:
			print_size_categories = False

		os.system('clear')

		del_table = PrettyTable()
		del_table.title = "Deletion Bin Membership"
		del_table.field_names = DELETION_BIN_HEADER

		if print_size_categories:
			del_table.add_row(DELETION_BIN_FILENAME_SIZES)
			del_table.hrules = True

		del_table.add_row(deletion_bins)
		print(del_table)

		print("\n\n")

		dup_table = PrettyTable()
		dup_table.title = "Duplication Bin Membership"
		dup_table.field_names = DUPLICATION_BIN_HEADER
		if print_size_categories:
			dup_table.add_row(DUPLICATION_BIN_FILENAME_SIZES)
			dup_table.hrules = True

		dup_table.add_row(duplication_bins)
		print(dup_table)

		print("\n\n")

		inv_table = PrettyTable()
		inv_table.title = "Inversion Bin Membership"
		inv_table.field_names = INVERSION_BIN_HEADER

		if print_size_categories:
			inv_table.add_row(INVERSION_BIN_FILENAME_SIZES)
			inv_table.hrules = True

		inv_table.add_row(inversion_bins)
		print(inv_table)
		print("\n")


		input("Press any key to return to menu\n")
	else:
		return deletion_bins, duplication_bins, inversion_bins

# Create csv files for each profile file containing the profile file name and bin memberships for each type of variant
# Writes to ./summary folder
def write_profile_names_and_bin_membership():
	os.system('clear')
	
	deletion_bins = deletion_bin_events # populates list with zeros with the number of bins created earlier
	duplication_bins = duplication_bin_events
	inversion_bins = inversion_bin_events
		
	deletion_row = [] # List to store the name of each profile file and the bin membership for the deletions it contains
	duplication_row = [] 
	inversion_row = [] 

	working_dir = os.getcwd()
	csvdir = str(working_dir) + "/" + "output/"
	if os.path.isdir(csvdir):
		for path in os.listdir(csvdir):
			full_path = os.path.join(csvdir, path)
			if os.path.isfile(full_path) and path.endswith(".csv"):
				with open(full_path, newline='') as csvfile:
					bin_reader = csv.reader(csvfile, delimiter=',')
					csv_rows=[row for row in bin_reader]
					row_integers = [] # create list to store csv row elements as integers (they are read as strings with csv.reader)
					for row in csv_rows:					
						row = [int(i) for i in row]
						row_integers.append(row)

					csv_dels = row_integers[0] # deletion bins in csv file
					deletion_bins = np.add(deletion_bins,csv_dels)
					
					profile_file_name = path.strip(".csv") + ".txt"

					new_deletion_row =  row_integers[0]
					new_deletion_row.insert(0, profile_file_name)
					deletion_row.append(new_deletion_row)

					csv_dups = row_integers[1] # duplication bins in csv file
					duplication_bins = np.add(duplication_bins,csv_dups)

					new_duplication_row =  row_integers[1]
					new_duplication_row.insert(0, profile_file_name)
					duplication_row.append(new_duplication_row)


					csv_invs = row_integers[2] # inversion bins in csv file
					inversion_bins = np.add(inversion_bins,csv_invs)

					new_inversion_row =  row_integers[2]
					new_inversion_row.insert(0, profile_file_name)
					inversion_row.append(new_inversion_row)
	else:
		print("Requires csv files in ./output")

	outdir = str(working_dir) + "/" + "summary/"
	print("Writing summary files (deletions.csv,duplications.csv,inversions.csv) for each variant to:\n" + str(outdir) + "\n")	

	deletions_file = outdir + "deletions.csv"
	duplications_file = outdir + "duplications.csv"
	inversions_file = outdir + "inversions.csv"
	
	total_bins = summarize_bin_membership(False)


	if not isinstance(total_bins[1], list): # if csv files are present, this variable element should be a numpy array; if not it is a list

		duplication_header=["Filename"] + DUPLICATION_BIN_HEADER
		duplication_row.insert(0, duplication_header)
		total_dups = ["Total"] + total_bins[1].tolist()
		duplication_row.append(total_dups)

		deletion_header=["Filename"] + DELETION_BIN_HEADER
		deletion_row.insert(0, deletion_header)
		total_dels = ["Total"] + total_bins[0].tolist()
		deletion_row.append(total_dels)

		inversion_header=["Filename"] + INVERSION_BIN_HEADER
		inversion_row.insert(0, inversion_header)
		total_invs = ["Total"] + total_bins[2].tolist()
		inversion_row.append(total_invs)

		if os.path.isfile(deletions_file) or os.path.isfile(duplications_file) or os.path.isfile(inversions_file):
			choice = input("Output file(s) already exist. Enter y to overwrite. Overwrite? ")
			if choice == "y" or choice == "Y":
				with open(deletions_file, 'w', newline='') as f:
					writer = csv.writer(f)
					writer.writerows(deletion_row)
				with open(duplications_file, 'w', newline='') as f:
					writer = csv.writer(f)
					writer.writerows(duplication_row)
				with open(inversions_file, 'w', newline='') as f:
					writer = csv.writer(f)
					writer.writerows(inversion_row)

		else:
			with open(deletions_file, 'w', newline='') as f:
				writer = csv.writer(f)
				writer.writerows(deletion_row)
			with open(duplications_file, 'w', newline='') as f:
				writer = csv.writer(f)
				writer.writerows(duplication_row)
			with open(inversions_file, 'w', newline='') as f:
				writer = csv.writer(f)
				writer.writerows(inversion_row)

		option = input("Print bin membership to screen? Press \"y\" for yes\n")
		if option == "Y" or option == "y":
			os.system('clear')
			del_table = PrettyTable()
			del_table.title = "Deletion Bin Membership"
			del_table.field_names = deletion_row[0]

			list_iterator = iter(deletion_row[0:len(deletion_row)-1]) # create iterator, excluding last row
			next(list_iterator) # skip header

			for row in list_iterator:
				del_table.add_row(row)
			print(del_table)
			del_table.add_row(total_dels)
			print("\n".join(del_table.get_string().splitlines()[-2:]))

			print("\n\n")

			dup_table = PrettyTable()
			dup_table.title = "Duplication Bin Membership"
			dup_table.field_names = duplication_row[0]

			list_iterator = iter(duplication_row[0:len(duplication_row)-1]) # create iterator, excluding last row
			next(list_iterator) # skip header

			for row in list_iterator:
				dup_table.add_row(row)
			print(dup_table)
			dup_table.add_row(total_dups)
			print("\n".join(dup_table.get_string().splitlines()[-2:]))

			print("\n\n")

			inv_table = PrettyTable()
			inv_table.title = "Inversion Bin Membership"
			inv_table.field_names = inversion_row[0]

			list_iterator = iter(inversion_row[0:len(inversion_row)-1]) # create iterator, excluding last row
			next(list_iterator) # skip header

			for row in list_iterator:
				inv_table.add_row(row)
			print(inv_table)
			inv_table.add_row(total_invs)
			print("\n".join(inv_table.get_string().splitlines()[-2:]))
			print("\n")

	else:
		print("No svsim profile files to summarize")

	input("Press any key to return to menu\n")



quit = "f"
while quit == "f":
	os.system('clear')
	print(MENU)
	option = input("Select an option. Note: case is insensitive.\n")
	if option == "D" or option == "d":
		new_deletion = get_variants_from_user("DEL",DELETION_BINS,DELETION_BIN_HEADER,DELETION_BIN_FILENAME_SIZES)
		if new_deletion:		
			profile_file_lines.append(new_deletion[0])
			new_deletion_stats = summarize_new_variant(new_deletion[1], DELETION_BINS)
			total_bases_in_deletions += new_deletion_stats[0]
			total_deletions += new_deletion_stats[1]
			deletion_df =  update_dataframe(deletion_df, new_deletion_stats[2])


	if option == "U" or option == "u":
		new_duplication = get_variants_from_user("DUP",DUPLICATION_BINS,DUPLICATION_BIN_HEADER,DUPLICATION_BIN_FILENAME_SIZES)
		if new_duplication:		
			profile_file_lines.append(new_duplication[0])
			new_duplication_stats = summarize_new_variant(new_duplication[1], DUPLICATION_BINS)
			total_bases_in_duplications += new_duplication_stats[0]
			total_duplications += new_duplication_stats[1]
			duplication_df =  update_dataframe(duplication_df, new_duplication_stats[2])


	if option == "I" or option == "i":
		new_inversion = get_variants_from_user("INV",INVERSION_BINS,INVERSION_BIN_HEADER,INVERSION_BIN_FILENAME_SIZES)
		if new_inversion:		
			profile_file_lines.append(new_inversion[0])
			new_inversion_stats = summarize_new_variant(new_inversion[1], INVERSION_BINS)
			total_bases_in_inversions += new_inversion_stats[0]
			total_inversions += new_inversion_stats[1]
			inversion_df =  update_dataframe(inversion_df, new_inversion_stats[2])

	if option == "B" or option == "b":
		summarize_bin_membership(True)

	if option == "C" or option == "c":
		write_profile_names_and_bin_membership()

	if option == "S" or option == "s":
		print_mock_genome_stats(total_bases_in_deletions,total_bases_in_duplications,total_bases_in_inversions,total_deletions,total_duplications,total_inversions)

	if option == "W" or option == "w":
		reset_dataframes = write_svsim_profile(deletion_df,duplication_df,inversion_df,profile_file_lines) 
		if reset_dataframes:
			duplication_df = pd.DataFrame({'Count': duplication_bin_events,'BP':duplication_bin_bases},index=pd.IntervalIndex.from_tuples(DUPLICATION_BINS, closed = 'left'))
			deletion_df = pd.DataFrame({'Count': deletion_bin_events,'BP':deletion_bin_bases},index=pd.IntervalIndex.from_tuples(DELETION_BINS, closed = 'left'))
			inversion_df = pd.DataFrame({'Count': inversion_bin_events,'BP':inversion_bin_bases},index=pd.IntervalIndex.from_tuples(INVERSION_BINS, closed = 'left'))
			total_bases_in_deletions = 0
			total_bases_in_duplications = 0
			total_bases_in_inversions = 0
			total_deletions = 0
			total_duplications = 0
			total_inversions = 0
			profile_file_lines = []

	elif option == "Q" or option == "q":
		quit = "t"
	else:
		print("Incorrect option")
