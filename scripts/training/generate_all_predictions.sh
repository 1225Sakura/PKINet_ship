#!/bin/bash
# 生成所有验证集的预测结果

source /home/user/anaconda3/etc/profile.d/conda.sh
conda activate pkinet

cd /home/user/PKINet

echo "=========================================="
echo "开始生成所有验证集的预测结果"
echo "=========================================="
echo ""

# LAFI数据集
echo "[1/3] 处理LAFI数据集 (1280张图像)..."
python tools/test.py \
    configs/pkinet/pkinet-s_lafi_ship.py \
    work_dirs/pkinet-s_lafi_ship/latest.pth \
    --show-dir work_dirs/all_vis_results/lafi \
    --show-score-thr 0.3 \
    > /tmp/lafi_vis.log 2>&1

echo "✓ LAFI完成"
echo ""

# DOTA Ship数据集
echo "[2/3] 处理DOTA Ship数据集 (108张图像)..."
python tools/test.py \
    configs/pkinet/pkinet-s_dota_ship.py \
    work_dirs/pkinet-s_dota_ship/latest.pth \
    --show-dir work_dirs/all_vis_results/dota_ship \
    --show-score-thr 0.3 \
    > /tmp/dota_vis.log 2>&1

echo "✓ DOTA Ship完成"
echo ""

# DOSR数据集
echo "[3/3] 处理DOSR数据集 (223张图像)..."
python tools/test.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/latest.pth \
    --show-dir work_dirs/all_vis_results/dosr \
    --show-score-thr 0.3 \
    > /tmp/dosr_vis.log 2>&1

echo "✓ DOSR完成"
echo ""

echo "=========================================="
echo "所有数据集处理完成！"
echo "=========================================="

# 统计结果
echo ""
echo "结果统计:"
echo "  LAFI:       $(ls work_dirs/all_vis_results/lafi/*.png 2>/dev/null | wc -l) 张图像"
echo "  DOTA Ship:  $(ls work_dirs/all_vis_results/dota_ship/*.png 2>/dev/null | wc -l) 张图像"
echo "  DOSR:       $(ls work_dirs/all_vis_results/dosr/*.png 2>/dev/null | wc -l) 张图像"
echo ""
echo "结果保存在: work_dirs/all_vis_results/"
