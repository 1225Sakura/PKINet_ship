#!/bin/bash
# 三个数据集的训练脚本

source /home/user/anaconda3/etc/profile.d/conda.sh
conda activate pkinet

cd /home/user/PKINet

echo "============================================"
echo "PKINet船舶检测训练脚本"
echo "============================================"
echo "1. 训练LAFI数据集 (49类船舶)"
echo "2. 训练DOTA ship数据集 (1类: ship)"
echo "3. 训练DOSR数据集 (20类船舶)"
echo "4. 依次训练全部三个数据集"
echo "============================================"
read -p "请选择 [1-4]: " choice

case $choice in
    1)
        echo "开始训练LAFI数据集..."
        python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py --gpu-ids 0
        ;;
    2)
        echo "开始训练DOTA ship数据集..."
        python tools/train.py configs/pkinet/pkinet-s_dota_ship.py --gpu-ids 0
        ;;
    3)
        echo "开始训练DOSR数据集..."
        python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py --gpu-ids 0
        ;;
    4)
        echo "开始依次训练全部三个数据集..."
        echo "===== 1/3: 训练LAFI数据集 ====="
        python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py --gpu-ids 0
        echo "===== 2/3: 训练DOTA ship数据集 ====="
        python tools/train.py configs/pkinet/pkinet-s_dota_ship.py --gpu-ids 0
        echo "===== 3/3: 训练DOSR数据集 ====="
        python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py --gpu-ids 0
        echo "全部训练完成！"
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
