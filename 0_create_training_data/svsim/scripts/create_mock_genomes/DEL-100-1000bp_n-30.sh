#!/usr/bin/env bash

#SBATCH --job-name=svsim_DEL-100-1000bp_n-30
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=single,lattice
#SBATCH --time=01:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=kyle.lesack@gmail.com
#SBATCH -o svsim_DEL-100-1000bp_n-30.%j.out
#SBATCH -e svsim_DEL-100-1000bp_n-30.%j.err

source ~/.bashrc

conda activate SVsim

REFERENCE=/home/kyle.lesack1/project_files/reference_genome/c_elegans.PRJNA13758.WS263.genomic.fa
PROFILE=/home/kyle.lesack1/project_files/repos/sv_pipeline/0_create_training_data/svsim/profiles/DEL-100-1000bp.txt
OUTPUT=/home/kyle.lesack1/project_files/repos/sv_pipeline/0_create_training_data/svsim/simulated_genomes/DEL-100-1000bp_n-30

mkdir -p $OUTPUT

python /home/kyle.lesack1/bin/SVsim-master/SVsim -i $PROFILE -r $REFERENCE -o $OUTPUT/SVSIM_DEL-100-1000bp_n-30 -W -n 30 -d
mv /home/kyle.lesack1/project_files/repos/sv_pipeline/0_create_training_data/svsim/simulated_genomes/DEL-100-1000bp_n-30/SVSIM_DEL-100-1000bp_n-30.fasta /home/kyle.lesack1/project_files/repos/sv_pipeline/0_create_training_data/svsim/simulated_genomes/DEL-100-1000bp_n-30/SVSIM_DEL-100-1000bp_n-30.fa


conda deactivate
