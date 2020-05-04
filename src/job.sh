#!/bin/bash
#SBATCH --account=def-jinguo
#SBATCH --gres=gpu:2              # Number of GPUs (per node)
#SBATCH --mem=16G               # memory (per node)
#SBATCH --time=7-00:00            # time (DD-HH:MM)
#SBATCH -o /home/jangeunb/projects/def-jinguo/jangeunb/CodeSearchNet/src/slurm-%j.out


source ~/ENV/bin/activate
module load cuda cudnn


python train.py --model SelfAttentionModel  --max-num-epochs 30
