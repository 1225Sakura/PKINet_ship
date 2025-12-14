#!/bin/bash
# 快速安装方案 - 使用pip安装

set -e

echo "======================================================"
echo "快速安装PKINet依赖（使用pip）"
echo "======================================================"
echo ""

# 激活环境
source $(conda info --base)/etc/profile.d/conda.sh
conda activate pkinet

echo "当前环境:"
which python
python --version
echo ""

# 使用pip安装PyTorch（更快）
echo "步骤 1/5: 安装PyTorch 1.11.0 + CUDA 11.3..."
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113

# 安装基础工具
echo ""
echo "步骤 2/5: 安装基础工具..."
pip install yapf==0.40.1

# 安装mmcv
echo ""
echo "步骤 3/5: 安装mmcv-full..."
pip install mmcv-full==1.7.0 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.11.0/index.html

# 安装mmdet和mmengine
echo ""
echo "步骤 4/5: 安装mmdet和mmengine..."
pip install mmdet==2.28.2
pip install mmengine

# 安装PKINet
echo ""
echo "步骤 5/5: 安装PKINet (mmrotate)..."
cd /home/user/PKINet
pip install -v -e .

echo ""
echo "======================================================"
echo "✅ 安装完成！"
echo "======================================================"
echo ""
echo "验证安装:"
python -c "import torch; print(f'✓ PyTorch: {torch.__version__}')"
python -c "import torch; print(f'✓ CUDA可用: {torch.cuda.is_available()}')"
python -c "import mmcv; print(f'✓ mmcv: {mmcv.__version__}')"
python -c "import mmdet; print(f'✓ mmdet: {mmdet.__version__}')"
python -c "import mmengine; print(f'✓ mmengine: {mmengine.__version__}')"
python -c "import mmrotate; print(f'✓ mmrotate安装成功')"
echo ""
