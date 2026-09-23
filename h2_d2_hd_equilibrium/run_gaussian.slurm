#!/bin/bash
# maestro: raw
#SBATCH --job-name=h2d2_hd_eq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --mem=2G
#SBATCH --output=slurm-%j.out

set -euo pipefail
module load gaussian16/g16
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
for input in h2.gjf d2.gjf hd.gjf; do
  g16 < "$input" > "${input%.gjf}.log"
done
