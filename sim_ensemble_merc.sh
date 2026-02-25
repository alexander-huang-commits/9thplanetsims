#!/bin/bash

#SBATCH --job-name=REBOUND_Ensemble_REAL
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ahuang54@uw.edu

#SBATCH --account=uwb
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --array=0-19
#SBATCH --time=13-12:00:00 # Max runtime in DD-HH:MM:SS format.

#SBATCH --chdir=/gscratch/uwb/ahuang54/saves/sims
#SBATCH --export=all
#SBATCH --output=Rlogs/MERC/out_%A_%a.txt
#SBATCH --error=Rlogs/MERC/err_%A_%a.txt

eval "$(/gscratch/uwb/ahuang54/miniconda3/bin/conda shell.bash hook)"
conda activate rebound


OUTDIR=results/run_MERCRUN_${SLURM_ARRAY_TASK_ID}
mkdir -p $OUTDIR

python simulation_merc.py \
    --job_id ${SLURM_ARRAY_TASK_ID} \
    --outdir $OUTDIR \
    --time_step 1e6 \
    --total_time 4e9 \
    --archive_interval 2e7