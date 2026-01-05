#!/bin/bash
# 测试训练脚本

source /home/user/anaconda3/etc/profile.d/conda.sh
conda activate pkinet

cd /home/user/PKINet

echo "测试LAFI训练..."
python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py --work-dir work_dirs/test_lafi --gpu-ids 0
