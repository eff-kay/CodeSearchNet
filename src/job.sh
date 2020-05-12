#!/bin/bash
#SBATCH --account=def-jinguo
#SBATCH --gres=gpu:v100l:4              # Number of GPUs (per node)
#SBATCH --mem=32G               # memory (per node)
#SBATCH --time=2-00:00            # time (DD-HH:MM)
#SBATCH --job-name=multi_head_only
#SBATCH -o /home/jangeunb/projects/def-jinguo/jangeunb/CodeSearchNet/src/output/%j_multi_head_only.out

source ~/tensorflow/bin/activate

module load cuda/10.0.130
module load cuda cudnn


ulimit -c unlimited
start_time=$(date)

python train.py --model SelfAttentionModel  --max-num-epochs 30 --run-name multi_head_only --quiet

end_time=$(date)

echo "Start Time: $start_time"
echo "End Time: $end_time"
