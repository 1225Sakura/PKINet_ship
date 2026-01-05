#!/bin/bash
# 在现有PyTorch环境中安装PKINet依赖

set -e

echo "======================================================"
echo "在现有环境中安装PKINet依赖"
echo "======================================================"
echo ""
echo "检测到的环境："
python -c "import torch; print(f'PyTorch版本: {torch.__version__}')"
python -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"
python -c "import torch; print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
echo ""

# 安装基础工具
echo "步骤 1/4: 安装基础工具..."
pip install yapf==0.40.1
pip install -U openmim

# 安装mmcv
echo ""
echo "步骤 2/4: 安装mmcv-full..."
echo "注意: 根据你的PyTorch和CUDA版本自动选择合适的mmcv版本"
pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu128/torch2.8.0/index.html || \
pip install mmcv || \
mim install mmcv-full

# 安装mmdet和mmengine
echo ""
echo "步骤 3/4: 安装mmdet和mmengine..."
pip install mmengine
pip install mmdet

# 安装PKINet (mmrotate)
echo ""
echo "步骤 4/4: 安装PKINet (mmrotate)..."
cd /home/user/PKINet
pip install -v -e .

echo ""
echo "======================================================"
echo "安装完成！"
echo "======================================================"
echo ""
echo "验证安装:"
python -c "import mmcv; print(f'mmcv版本: {mmcv.__version__}')"
python -c "import mmdet; print(f'mmdet版本: {mmdet.__version__}')"
python -c "import mmengine; print(f'mmengine版本: {mmengine.__version__}')"
python -c "import mmrotate; print(f'mmrotate安装成功')"
echo ""
