# PKINet 遥感图像船舶检测

[English](README.md) | 简体中文

## 项目简介

本仓库使用 [PKINet (Poly Kernel Inception Network)](https://openaccess.thecvf.com/content/CVPR2024/papers/Cai_Poly_Kernel_Inception_Network_for_Remote_Sensing_Detection_CVPR_2024_paper.pdf) 实现**船舶检测**任务。PKINet 是专为遥感图像设计的旋转目标检测框架，发表于 CVPR 2024。

我们在三个不同的船舶检测数据集上微调了 PKINet-S 模型：

- **LAFI**：49个细粒度船舶类别
- **DOTA Ship-only**：从 DOTA v1.0 提取的单一船舶类别
- **DOSR**：20种船舶类型（包括货船、油轮、潜艇等）

## 训练结果

### 性能总结

| 数据集        | 类别数 | 训练图像数 | 最佳mAP    | 配置文件                                         |
| ------------- | ------ | ---------- | ---------- | ------------------------------------------------ |
| **DOSR**      | 20     | 523        | **51.23%** | [config](./configs/pkinet/pkinet-s_dosr_ship.py) |
| **DOTA Ship** | 1      | 326        | **43.04%** | [config](./configs/pkinet/pkinet-s_dota_ship.py) |
| **LAFI**      | 49     | 5,120      | **26.79%** | [config](./configs/pkinet/pkinet-s_lafi_ship.py) |

### 详细结果

#### 1. DOSR 数据集（20个船舶类别）

- **最佳mAP**：51.23%（第27轮）
- **训练集**：523张图像，训练30轮
- **验证集**：223张图像
- **模型路径**：`work_dirs/pkinet-s_dosr_ship/epoch_30.pth`
- **类别**：tanker、cargo、submarine、aircraft carrier、destroyer 等

#### 2. DOTA Ship 数据集（单一类别）

- **最佳mAP**：43.04%（第27轮）
- **训练集**：326张图像，包含28,068个船舶实例
- **验证集**：108张图像，包含8,960个船舶实例
- **模型路径**：`work_dirs/pkinet-s_dota_ship/epoch_30.pth`
- **类别**：ship（通用船舶）

#### 3. LAFI 数据集（49个细粒度船舶类别）

- **最佳mAP**：26.79%（第6轮）
- **训练集**：5,120张图像
- **验证集**：1,280张图像
- **模型路径**：`work_dirs/pkinet-s_lafi_ship/epoch_8.pth`
- **类别**：Nimitz、Enterprise、Arleigh_Burke_DD、Container_Ship、Ferry、Yacht 等

## 数据集说明

### 数据集和模型下载

**百度网盘链接**: [https://pan.baidu.com/s/5ZEE6OdCf9QEWK-0rm2I0qA](https://pan.baidu.com/s/5ZEE6OdCf9QEWK-0rm2I0qA)

百度网盘分享包含两个文件夹：

#### 📁 数据集文件夹

包含三个船舶检测数据集：

- `LAFI_dataset.tar.gz` (850MB) - 49个细粒度船舶类别，5,120训练图像 + 1,280验证图像
- `dota_ship_only_dataset.tar.gz` (710MB) - 单一船舶类别，326训练图像 + 108验证图像
- `DOSR_converted_dataset.tar.gz` (585MB) - 20种船舶类型，523训练图像 + 223验证图像

#### 📁 模型文件夹

包含预训练权重和训练好的模型：

- `pkinet_s_pretrain.pth` - ImageNet预训练的PKINet-S主干网络
- `work_dirs/` - 三个数据集的训练模型：
  - `pkinet-s_lafi_ship/` - 最佳mAP: 26.79%（第6轮）
  - `pkinet-s_dota_ship/` - 最佳mAP: 43.04%（第27轮）
  - `pkinet-s_dosr_ship/` - 最佳mAP: 51.23%（第27轮）

#### 安装步骤

1. 从百度网盘下载数据集并解压到 `data/` 目录：

```bash
tar -xzf LAFI_dataset.tar.gz -C data/
tar -xzf dota_ship_only_dataset.tar.gz -C data/
tar -xzf DOSR_converted_dataset.tar.gz -C data/
```

2. 下载预训练主干网络并放置到 `checkpoints/` 目录：

```bash
mkdir -p checkpoints
# 将 pkinet_s_pretrain.pth 移动到 checkpoints/
mv pkinet_s_pretrain.pth checkpoints/
```

3. （可选）下载训练好的模型并放置到 `work_dirs/`：

```bash
# 从百度网盘解压 work_dirs 文件夹
# 包含所有训练好的模型权重
```

### 数据集详情

### 1. LAFI 数据集

- **位置**：`data/LAFI/`
- **训练集**：5,120张图像
- **验证集**：1,280张图像
- **类别数**：49个细粒度船舶类型

### 2. DOTA Ship-only 数据集

- **位置**：`data/dota_ship_only/`
- **训练集**：326张图像，28,068个船舶实例
- **验证集**：108张图像，8,960个船舶实例
- **类别数**：1个（ship）
- **来源**：从 DOTA v1.0 数据集筛选得到

### 3. DOSR 数据集

- **位置**：`data/DOSR_converted/`
- **训练集**：523张图像
- **验证集**：223张图像
- **类别数**：20种船舶类型
- **格式**：从 XML 格式转换为 DOTA 格式

## 安装

### 快速安装

我们提供了快速安装脚本：

```bash
bash quick_install.sh
```

### 手动安装

本项目依赖 [PyTorch](https://pytorch.org/)、[MMCV](https://github.com/open-mmlab/mmcv)、[MMDetection](https://github.com/open-mmlab/mmdetection) 和 [MMRotate](https://github.com/open-mmlab/mmrotate)。

```bash
# 创建 conda 环境
conda create --name pkinet python=3.8 -y
conda activate pkinet

# 安装 PyTorch
conda install pytorch==1.11.0 torchvision==0.12.0 cudatoolkit=11.3 -c pytorch

# 安装依赖
pip install yapf==0.40.1
pip install -U openmim
mim install mmcv-full
mim install mmdet
mim install mmengine

# 安装本项目
cd PKINet
mim install -v -e .
```

## 训练

### 训练所有数据集

使用交互式训练脚本：

```bash
bash train_all_datasets.sh
```

### 训练单个数据集

```bash
# 训练 DOSR 数据集
python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py --work-dir work_dirs/pkinet-s_dosr_ship --gpu-ids 0

# 训练 DOTA Ship 数据集
python tools/train.py configs/pkinet/pkinet-s_dota_ship.py --work-dir work_dirs/pkinet-s_dota_ship --gpu-ids 0

# 训练 LAFI 数据集
python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py --work-dir work_dirs/pkinet-s_lafi_ship --gpu-ids 0
```

## 测试和推理

### 在验证集上测试

```bash
python tools/test.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/epoch_30.pth \
    --eval mAP
```

### 可视化结果

```bash
python tools/test.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/epoch_30.pth \
    --show-dir vis_results/
```

### 生成预测结果

为所有三个数据集生成预测结果：

```bash
bash generate_all_predictions.sh
```

## 项目结构

```
PKINet/
├── configs/pkinet/              # 训练配置文件
│   ├── pkinet-s_lafi_ship.py
│   ├── pkinet-s_dota_ship.py
│   └── pkinet-s_dosr_ship.py
├── data/                        # 数据集
│   ├── LAFI/
│   ├── dota_ship_only/
│   └── DOSR_converted/
├── work_dirs/                   # 训练输出和模型
├── tools/                       # 训练和测试脚本
├── mmrotate/                    # 核心框架代码
├── checkpoints/                 # 预训练主干网络权重
├── README_TRAINING.md           # 详细训练指南
└── TRAINING_RESULTS.md          # 完整训练日志
```

## 主要特性

- **多数据集支持**：在 LAFI、DOTA Ship 和 DOSR 数据集上训练
- **旋转边界框**：精确的船舶方向检测
- **细粒度分类**：最多支持49个船舶类别（LAFI）
- **高性能**：在 DOSR 数据集上达到 51.23% mAP
- **易于使用**：提供训练、测试和可视化脚本
- **预训练主干**：ImageNet 预训练的 PKINet-S 主干网络

## 文档

- **[训练指南](README_TRAINING.md)**：完整的环境配置和训练指南
- **[训练结果](TRAINING_RESULTS.md)**：详细的训练日志和性能分析
- MMRotate 基础知识请参考[官方文档](https://mmrotate.readthedocs.io/)

## 开源许可证

本项目采用 [Apache 2.0 许可证](LICENSE)。

## 致谢

本项目基于以下工作：

- **PKINet**：[Poly Kernel Inception Network for Remote Sensing Detection (CVPR 2024)](https://openaccess.thecvf.com/content/CVPR2024/papers/Cai_Poly_Kernel_Inception_Network_for_Remote_Sensing_Detection_CVPR_2024_paper.pdf)
- **MMRotate**：[OpenMMLab 旋转目标检测工具箱](https://github.com/open-mmlab/mmrotate)
- **DOTA**：[A Large-scale Dataset for Object Detection in Aerial Images](https://captain-whu.github.io/DOTA/index.html)

## 引用

如果您使用了本工作或训练好的模型，请引用原始 PKINet 论文：

```bibtex
@InProceedings{Cai_2024_Poly,
    author    = {Cai, Xinhao and Lai, Qiuxia and Wang, Yuwei and Wang, Wenguan and Sun, Zeren and Yao, Yazhou},
    title     = {Poly Kernel Inception Network for Remote Sensing Detection},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2024},
    pages     = {27706-27716}
}
```

## 联系方式

关于本船舶检测实现的问题，请在本仓库提交 issue。

关于原始 PKINet 方法的问题，请参考[原始仓库](https://github.com/caixiaoh/PKINet)。
