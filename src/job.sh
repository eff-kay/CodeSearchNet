#!/bin/bash
#SBATCH --partition=main
#SBATCH --gres=gpu:v100-32gb:2
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --job-name=informed_gpu:2_batch:1000
#SBATCH -o /network/home/jangeunb/CodeSearchNet/src/output/%j_informed_gpu:2_batch:1000.out


module load python/3.7

pip install -r requirements.txt

module load cuda/10.0/cudnn/7.5 

exit_script() {
    echo "Preemption signal, saving myself"
    trap - SIGTERM # clear the trap
    # Optional: sends SIGTERM to child/sub processes
    kill -- -$$
}

trap exit_script SIGTERM



ulimit -c unlimited

start_time=$(date)

python train.py --model SelfAttentionModel  --max-num-epochs 30 --run-name informed_gpu:2_batch:1000 --quiet

end_time=$(date)

echo "Start Time: $start_time"
echo "End Time: $end_time"
