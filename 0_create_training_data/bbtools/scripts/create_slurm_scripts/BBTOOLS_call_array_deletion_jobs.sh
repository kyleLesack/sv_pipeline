#!/bin/bash
#SBATCH --job-name=BBTOOLS_call_array_deletion_jobs
#SBATCH --mem=6G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=single,lattice
#SBATCH --time=01:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=kyle.lesack@gmail.com
#SBATCH -o BBTOOLS_call_array_deletion_jobs.%j.out
#SBATCH -e BBTOOLS_call_array_deletion_jobs.%j.err
#SBATCH --array=1-25

bash ./deletions/DEL*.$SLURM_ARRAY_TASK_ID
