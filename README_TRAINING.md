# PKINet 船舶检测训练 - 完整指南

## 数据集准备完成

### 1. **LAFI数据集**
- **位置**: `/home/user/PKINet/data/LAFI/`
- **训练集**: 5,120 张图像
- **验证集**: 1,280 张图像
- **类别数**: 49 个船舶类别
- **类别示例**: Nimitz, Arleigh_Burke_DD, Container_Ship, Cargo, Ferry, Yacht等
- **配置文件**: `configs/pkinet/pkinet-s_lafi_ship.py`

### 2. **DOTA ship-only数据集**
- **位置**: `/home/user/PKINet/data/dota_ship_only/`
- **训练集**: 326 张图像，28,068 个船舶目标
- **验证集**: 108 张图像，8,960 个船舶目标
- **类别数**: 1 个（ship）
- **配置文件**: `configs/pkinet/pkinet-s_dota_ship.py`
- **来源**: 从DOTA v1.0数据集中筛选船舶类别

### 3. **DOSR数据集**
- **位置**: `/home/user/PKINet/data/DOSR_converted/`
- **训练集**: 523 张图像
- **验证集**: 223 张图像
- **类别数**: 2 个（flat traffic ship, yacht）
- **配置文件**: `configs/pkinet/pkinet-s_dosr_ship.py`
- **来源**: 从XML格式转换为DOTA格式

---

## Conda环境设置

### 环境安装
环境安装脚本已在后台运行：
```bash
# 检查安装进度
tail -f setup_env.log
```

如果需要手动安装或重新安装：
```bash
bash setup_env.sh
```

### 环境信息
- **环境名称**: pkinet
- **Python版本**: 3.8
- **PyTorch版本**: 1.11.0
- **CUDA版本**: 11.3
- **依赖包**: mmcv-full, mmdet, mmengine, mmrotate

### 激活环境
```bash
conda activate pkinet
```

### 验证安装
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
python -c "import mmrotate; print(f'MMRotate安装成功')"
```

---

## 训练配置文件

所有配置文件都位于 `configs/pkinet/` 目录下：

1. **pkinet-s_lafi_ship.py** - LAFI数据集（49类）
2. **pkinet-s_dota_ship.py** - DOTA ship（1类）
3. **pkinet-s_dosr_ship.py** - DOSR数据集（2类）

### 配置参数
- **Batch Size**: 2
- **学习率**: 0.0002
- **优化器**: AdamW
- **训练轮数**: 30 epochs
- **验证间隔**: 每3个epoch
- **图像尺寸**: 1024x1024

---

## 开始训练

### 方式1: 使用交互式训练脚本（推荐）
```bash
cd /home/user/PKINet
conda activate pkinet
./train_all_datasets.sh
```

这个脚本会提供以下选项：
1. 仅训练 LAFI
2. 仅训练 DOTA ship
3. 仅训练 DOSR
4. 训练所有三个数据集（依次执行）
5. 训练所有三个数据集（并行执行，需要多个GPU）

### 方式2: 手动启动单个训练任务

#### 训练LAFI数据集
```bash
conda activate pkinet
python tools/train.py \
    configs/pkinet/pkinet-s_lafi_ship.py \
    --work-dir work_dirs/pkinet-s_lafi_ship \
    --gpu-ids 0
```

#### 训练DOTA ship数据集
```bash
conda activate pkinet
python tools/train.py \
    configs/pkinet/pkinet-s_dota_ship.py \
    --work-dir work_dirs/pkinet-s_dota_ship \
    --gpu-ids 0
```

#### 训练DOSR数据集
```bash
conda activate pkinet
python tools/train.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    --work-dir work_dirs/pkinet-s_dosr_ship \
    --gpu-ids 0
```

### 方式3: 后台并行训练（多GPU）

如果有多个GPU，可以同时训练所有数据集：

```bash
conda activate pkinet

# GPU 0: LAFI
nohup python tools/train.py \
    configs/pkinet/pkinet-s_lafi_ship.py \
    --work-dir work_dirs/pkinet-s_lafi_ship \
    --gpu-ids 0 \
    > train_lafi.log 2>&1 &

# GPU 1: DOTA ship
nohup python tools/train.py \
    configs/pkinet/pkinet-s_dota_ship.py \
    --work-dir work_dirs/pkinet-s_dota_ship \
    --gpu-ids 1 \
    > train_dota_ship.log 2>&1 &

# GPU 2: DOSR
nohup python tools/train.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    --work-dir work_dirs/pkinet-s_dosr_ship \
    --gpu-ids 2 \
    > train_dosr.log 2>&1 &
```

---

## 监控训练

### 查看训练日志
```bash
# LAFI训练日志
tail -f train_lafi.log

# DOTA ship训练日志
tail -f train_dota_ship.log

# DOSR训练日志
tail -f train_dosr.log
```

### 查看TensorBoard
```bash
tensorboard --logdir work_dirs/
```

### 检查训练状态
```bash
# 查看GPU使用情况
nvidia-smi

# 查看进程
ps aux | grep train.py
```

---

## 训练输出

训练完成后，模型和日志将保存在以下目录：

- **LAFI**: `work_dirs/pkinet-s_lafi_ship/`
- **DOTA ship**: `work_dirs/pkinet-s_dota_ship/`
- **DOSR**: `work_dirs/pkinet-s_dosr_ship/`

每个目录包含：
- `*.pth` - 模型权重文件
- `*.log.json` - 训练日志
- `*.py` - 配置文件副本
- `tf_logs/` - TensorBoard日志

---

## 预训练权重（可选）

如需使用预训练权重，下载后修改配置文件中的 `checkpoint` 参数：

- **PKINet-T**: [下载链接](https://1drv.ms/u/c/9ce9a57f1a400a74/EXQKQBp_pekggJxvAAAAAAABWyCuNnKnuiA47qX6Wr7TMQ?e=pWhU1h)
- **PKINet-S**: [下载链接](https://1drv.ms/u/c/9ce9a57f1a400a74/EXQKQBp_pekggJxrAAAAAAAB46whGHAZkAw-Pnkwgc_OWQ?e=n0NrZl)

---

## 测试和推理

训练完成后，使用以下命令进行测试：

```bash
python tools/test.py \
    configs/pkinet/pkinet-s_lafi_ship.py \
    work_dirs/pkinet-s_lafi_ship/latest.pth \
    --eval mAP
```

---

## 常见问题

### 1. CUDA Out of Memory
降低batch size或图像尺寸：
```python
# 在配置文件中修改
bs = 1  # 降低batch size
dict(type='RResize', img_scale=(512, 512))  # 降低图像尺寸
```

### 2. 查看数据集统计
```bash
# LAFI
ls data/LAFI/train/annfiles | wc -l
ls data/LAFI/val/annfiles | wc -l

# DOTA ship
ls data/dota_ship_only/train/annfiles | wc -l
ls data/dota_ship_only/val/annfiles | wc -l

# DOSR
ls data/DOSR_converted/train/annfiles | wc -l
ls data/DOSR_converted/val/annfiles | wc -l
```

### 3. 环境问题
如果遇到导入错误，重新安装环境：
```bash
conda env remove -n pkinet
bash setup_env.sh
```

---

## 文件结构

```
/home/user/PKINet/
├── data/                           # 数据集目录
│   ├── LAFI/                      # LAFI数据集
│   ├── dota_ship_only/            # DOTA ship数据集
│   └── DOSR_converted/            # DOSR数据集
├── configs/pkinet/                # 配置文件
│   ├── pkinet-s_lafi_ship.py
│   ├── pkinet-s_dota_ship.py
│   └── pkinet-s_dosr_ship.py
├── tools/                         # 训练和测试脚本
│   ├── train.py
│   └── test.py
├── work_dirs/                     # 训练输出
├── setup_env.sh                   # 环境安装脚本
├── train_all_datasets.sh          # 训练脚本
├── filter_ship_data.py            # DOTA数据筛选脚本
├── convert_dosr.py                # DOSR格式转换脚本
└── README_TRAINING.md             # 本文档
```

---

## 联系和支持

- **PKINet论文**: [CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Cai_Poly_Kernel_Inception_Network_for_Remote_Sensing_Detection_CVPR_2024_paper.pdf)
- **代码仓库**: 当前PKINet项目
- **MMRotate文档**: [https://mmrotate.readthedocs.io/](https://mmrotate.readthedocs.io/)

---

祝训练顺利！ 🚢
