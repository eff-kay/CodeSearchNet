#!/bin/bash


#SBATCH --partition=unkillable
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:v100-32gb:4
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH -o /network/home/jangeunb/CodeSearchNet/src/slurm-%j.out

module load python/3.7

pip install -r requirements.txt

python train.py --model SelfAttentionModel
