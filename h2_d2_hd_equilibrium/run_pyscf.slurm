#!/bin/bash
# maestro: raw
#SBATCH --job-name=h2d2_hd_pyscf
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --mem=2G
#SBATCH --output=pyscf-%j.out

set -euo pipefail
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
/appl/share/maestro/maestro/.venv/bin/maestro-python pyscf_isotope_equilibrium.py
