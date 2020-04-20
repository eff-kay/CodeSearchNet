#!/bin/bash


#SBATCH --partition=unkillable
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:v100-32gb:2
#SBATCH --mem=32G
#SBATCH --time=96:00:00
#SBATCH -o /network/home/jangeunb/slurm_non_strict-%j.out

module load python/3.7

pip install -r requirements.txt

python train.py --model SelfAttentionModel --max-num-epochs 30
