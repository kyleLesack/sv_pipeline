#!/bin/bash
#SBATCH --job-name=BBTOOLS_INV-100-1000bp_n-30_15X
#SBATCH --mem=6G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=single,lattice
#SBATCH --time=01:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=kyle.lesack@gmail.com
#SBATCH -o BBTOOLS_INV-100-1000bp_n-30_15X.%j.out
#SBATCH -e BBTOOLS_INV-100-1000bp_n-30_15X.%j.err


REFERENCE=/home/kyle.lesack1/project_files/repos/sv_pipeline/0_create_training_data/svsim/simulated_genomes/INV-100-1000bp_n-30/SVSIM_INV-100-1000bp_n-30.fa
OUTPUT_DIR=/home/kyle.lesack1/project_files/repos/sv_pipeline/0_create_training_data/bbtools/randomreads_output/15X/INV-100-1000bp_n-30/
mkdir -p $OUTPUT_DIR

#Usage:   randomreads.sh ref=<file> out=<file> length=<number> reads=<number>

source ~/.bashrc
cd $OUTPUT_DIR

conda activate bbtools

randomreads.sh ref=$REFERENCE out1=INV-100-1000bp_n-30_1.fq out2=INV-100-1000bp_n-30_2.fq length=100 coverage=15 paired=t illuminanames=t addslash=t mininsert=275 maxinsert=325 gaussian=t

conda deactivate



