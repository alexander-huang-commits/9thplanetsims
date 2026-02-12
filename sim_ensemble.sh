#!/bin/bash

#SBATCH --job-name=REBOUND_Ensemble
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ahuang54@uw.edu

#SBATCH --account=uwb
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --array=0-31
#SBATCH --time=05-06:00:00 # Max runtime in DD-HH:MM:SS format.

#SBATCH --chdir=/gscratch/uwb/ahuang54/saves/sims
#SBATCH --export=all
#SBATCH --output=logs/out_%A_%a.txt
#SBATCH --error=logs/err_%A_%a.txt

eval "$(/gscratch/uwb/ahuang54/miniconda3/bin/conda shell.bash hook)"
conda activate rebound


OUTDIR=results/run_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}
mkdir -p $OUTDIR

python simulation.py \
    --job_id ${SLURM_ARRAY_TASK_ID} \
    --outdir $OUTDIR \
    --time_step 1e4 \
    --total_time 1e5 \
    --archive_interval 1e4