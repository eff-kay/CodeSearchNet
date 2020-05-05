#!/bin/bash
#SBATCH --partition=long
#SBATCH --gres=gpu:v100-32gb:1
#SBATCH --mem=32G
#SBATCH --time=168:00:00
#SBATCH -o /network/home/jangeunb/CodeSearchNet/src/slurm-informed-%j.out

module load python/3.7

pip install -r requirements.txt



exit_script() {
    echo "Preemption signal, saving myself"
    trap - SIGTERM # clear the trap
    # Optional: sends SIGTERM to child/sub processes
    kill -- -$$
}

trap exit_script SIGTERM


python train.py --model SelfAttentionModel  --max-num-epochs 30
