#!/bin/bash
#SBATCH --job-name=Cluster
#SBATCH --output=/home/ahmadf/batch/sbatch.out%j
#SBATCH --error=/home/ahmadf/batch/sbatch.err%j
#SBATCH --time=23:55:00
#SBATCH --mem=75GB
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH -w node20

module load python
source activate drysdale_replication

python3 /home/ahmadf/CentraCare/clustering_tests.py

conda deactivate