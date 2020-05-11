#!/bin/bash
#SBATCH --account=def-jinguo
#SBATCH --gres=gpu:v100l:4              # Number of GPUs (per node)
#SBATCH --mem=32G               # memory (per node)
#SBATCH --time=2-00:00            # time (DD-HH:MM)
#SBATCH --job-name=multi-head-only
#SBATCH -o /home/jangeunb/projects/def-jinguo/jangeunb/CodeSearchNet/src/output/%j_multi-head-only.out

source ~/tensorflow/bin/activate

module load cuda cudnn


ulimit -c unlimited


python train.py --model SelfAttentionModel  --max-num-epochs 30 --run-name multi-head-only --quiet
