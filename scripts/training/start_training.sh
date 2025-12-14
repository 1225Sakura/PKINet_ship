#!/bin/bash
# 训练脚本 - 分别训练LAFI和DOTA ship数据集

echo "======================================================"
echo "PKINet 船舶检测训练脚本"
echo "======================================================"
echo ""
echo "数据集准备情况："
echo "1. LAFI数据集: 5120个训练图像, 1280个验证图像, 49个船舶类别"
echo "2. DOTA ship数据集: 326个训练图像, 108个验证图像, 1个类别"
echo ""
echo "======================================================"
echo ""

# 检查GPU
echo "检查GPU..."
nvidia-smi

echo ""
echo "======================================================"
echo "训练LAFI数据集"
echo "======================================================"
echo "配置文件: configs/pkinet/pkinet-s_lafi_ship.py"
echo "训练将使用30个epoch，每3个epoch验证一次"
echo ""

# 训练LAFI - 后台运行
nohup python tools/train.py \
    configs/pkinet/pkinet-s_lafi_ship.py \
    --work-dir work_dirs/pkinet-s_lafi_ship \
    --gpu-ids 0 \
    > train_lafi.log 2>&1 &

LAFI_PID=$!
echo "LAFI训练已启动，PID: $LAFI_PID"
echo "日志文件: train_lafi.log"
echo ""

echo "======================================================"
echo "训练DOTA ship数据集"
echo "======================================================"
echo "配置文件: configs/pkinet/pkinet-s_dota_ship.py"
echo "训练将使用30个epoch，每3个epoch验证一次"
echo ""

# 如果有多个GPU，可以使用GPU 1
# 如果只有一个GPU，需要等LAFI训练完成后再训练
read -p "是否立即启动DOTA ship训练？(如果只有一个GPU建议等LAFI完成)(y/n): " start_dota

if [ "$start_dota" = "y" ]; then
    nohup python tools/train.py \
        configs/pkinet/pkinet-s_dota_ship.py \
        --work-dir work_dirs/pkinet-s_dota_ship \
        --gpu-ids 0 \
        > train_dota_ship.log 2>&1 &

    DOTA_PID=$!
    echo "DOTA ship训练已启动，PID: $DOTA_PID"
    echo "日志文件: train_dota_ship.log"
else
    echo "DOTA ship训练将稍后手动启动"
    echo "使用以下命令启动："
    echo "python tools/train.py configs/pkinet/pkinet-s_dota_ship.py --work-dir work_dirs/pkinet-s_dota_ship --gpu-ids 0"
fi

echo ""
echo "======================================================"
echo "训练状态监控"
echo "======================================================"
echo "查看LAFI训练日志: tail -f train_lafi.log"
echo "查看DOTA训练日志: tail -f train_dota_ship.log"
echo ""
echo "训练进程:"
echo "  LAFI PID: $LAFI_PID"
if [ -n "$DOTA_PID" ]; then
    echo "  DOTA PID: $DOTA_PID"
fi
echo ""
echo "停止训练: kill <PID>"
echo "======================================================"
