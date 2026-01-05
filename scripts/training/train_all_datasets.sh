#!/bin/bash
# 三个数据集的完整训练脚本

echo "======================================================"
echo "PKINet 船舶检测 - 三个数据集训练脚本"
echo "======================================================"
echo ""

# 激活conda环境
echo "激活conda环境: pkinet"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate pkinet

# 检查环境
echo ""
echo "检查环境..."
python -c "import torch; print(f'PyTorch版本: {torch.__version__}')"
python -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"
python -c "import torch; print(f'CUDA版本: {torch.version.cuda}')" 2>/dev/null || echo "CUDA版本: N/A"

echo ""
echo "======================================================"
echo "数据集信息"
echo "======================================================"
echo ""
echo "1. LAFI数据集"
echo "   - 训练集: 5,120 张图像"
echo "   - 验证集: 1,280 张图像"
echo "   - 类别数: 49 个船舶类别"
echo "   - 配置文件: configs/pkinet/pkinet-s_lafi_ship.py"
echo ""
echo "2. DOTA ship数据集"
echo "   - 训练集: 326 张图像, 28,068 个船舶目标"
echo "   - 验证集: 108 张图像, 8,960 个船舶目标"
echo "   - 类别数: 1 个 (ship)"
echo "   - 配置文件: configs/pkinet/pkinet-s_dota_ship.py"
echo ""
echo "3. DOSR数据集"
echo "   - 训练集: 523 张图像"
echo "   - 验证集: 223 张图像"
echo "   - 类别数: 2 个 (flat traffic ship, yacht)"
echo "   - 配置文件: configs/pkinet/pkinet-s_dosr_ship.py"
echo ""
echo "======================================================"
echo ""

# 检查GPU
echo "GPU信息:"
nvidia-smi --query-gpu=index,name,memory.total,memory.free --format=csv,noheader 2>/dev/null || echo "未检测到GPU"

echo ""
echo "======================================================"
echo "训练选项"
echo "======================================================"
echo ""
echo "请选择要训练的数据集:"
echo "  1) 仅训练 LAFI"
echo "  2) 仅训练 DOTA ship"
echo "  3) 仅训练 DOSR"
echo "  4) 训练所有三个数据集（依次执行）"
echo "  5) 训练所有三个数据集（并行执行，需要多个GPU）"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "======================================================"
        echo "启动LAFI训练"
        echo "======================================================"
        python tools/train.py \
            configs/pkinet/pkinet-s_lafi_ship.py \
            --work-dir work_dirs/pkinet-s_lafi_ship \
            --gpu-ids 0
        ;;
    2)
        echo ""
        echo "======================================================"
        echo "启动DOTA ship训练"
        echo "======================================================"
        python tools/train.py \
            configs/pkinet/pkinet-s_dota_ship.py \
            --work-dir work_dirs/pkinet-s_dota_ship \
            --gpu-ids 0
        ;;
    3)
        echo ""
        echo "======================================================"
        echo "启动DOSR训练"
        echo "======================================================"
        python tools/train.py \
            configs/pkinet/pkinet-s_dosr_ship.py \
            --work-dir work_dirs/pkinet-s_dosr_ship \
            --gpu-ids 0
        ;;
    4)
        echo ""
        echo "======================================================"
        echo "依次训练三个数据集"
        echo "======================================================"

        echo ""
        echo "1/3: 训练LAFI..."
        python tools/train.py \
            configs/pkinet/pkinet-s_lafi_ship.py \
            --work-dir work_dirs/pkinet-s_lafi_ship \
            --gpu-ids 0

        echo ""
        echo "2/3: 训练DOTA ship..."
        python tools/train.py \
            configs/pkinet/pkinet-s_dota_ship.py \
            --work-dir work_dirs/pkinet-s_dota_ship \
            --gpu-ids 0

        echo ""
        echo "3/3: 训练DOSR..."
        python tools/train.py \
            configs/pkinet/pkinet-s_dosr_ship.py \
            --work-dir work_dirs/pkinet-s_dosr_ship \
            --gpu-ids 0
        ;;
    5)
        echo ""
        echo "======================================================"
        echo "并行训练三个数据集"
        echo "======================================================"
        echo "注意: 需要至少3个GPU，分别使用GPU 0, 1, 2"
        echo ""

        # 后台启动三个训练任务
        nohup python tools/train.py \
            configs/pkinet/pkinet-s_lafi_ship.py \
            --work-dir work_dirs/pkinet-s_lafi_ship \
            --gpu-ids 0 \
            > train_lafi.log 2>&1 &
        LAFI_PID=$!
        echo "LAFI训练已启动 (PID: $LAFI_PID, GPU: 0, 日志: train_lafi.log)"

        nohup python tools/train.py \
            configs/pkinet/pkinet-s_dota_ship.py \
            --work-dir work_dirs/pkinet-s_dota_ship \
            --gpu-ids 1 \
            > train_dota_ship.log 2>&1 &
        DOTA_PID=$!
        echo "DOTA ship训练已启动 (PID: $DOTA_PID, GPU: 1, 日志: train_dota_ship.log)"

        nohup python tools/train.py \
            configs/pkinet/pkinet-s_dosr_ship.py \
            --work-dir work_dirs/pkinet-s_dosr_ship \
            --gpu-ids 2 \
            > train_dosr.log 2>&1 &
        DOSR_PID=$!
        echo "DOSR训练已启动 (PID: $DOSR_PID, GPU: 2, 日志: train_dosr.log)"

        echo ""
        echo "所有训练任务已在后台启动"
        echo "查看日志:"
        echo "  tail -f train_lafi.log"
        echo "  tail -f train_dota_ship.log"
        echo "  tail -f train_dosr.log"
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================================"
echo "训练完成/退出"
echo "======================================================"
