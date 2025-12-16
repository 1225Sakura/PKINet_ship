# PKINet for Ship Detection in Remote Sensing Images

## Introduction

This repository implements **ship detection** using [PKINet (Poly Kernel Inception Network)](https://openaccess.thecvf.com/content/CVPR2024/papers/Cai_Poly_Kernel_Inception_Network_for_Remote_Sensing_Detection_CVPR_2024_paper.pdf) on multiple datasets. PKINet is a state-of-the-art rotated object detection framework specifically designed for remote sensing images, originally published at CVPR 2024.

We have fine-tuned PKINet-S models on three different ship detection datasets:

- **LAFI**: 49 fine-grained ship categories
- **DOTA Ship-only**: Single ship class from DOTA v1.0
- **DOSR**: 20 ship types including cargo, tanker, submarine, etc.

## Trained Models and Results

### Performance Summary

| Dataset       | Classes | Train Images | Best mAP   | Config                                           |
| ------------- | ------- | ------------ | ---------- | ------------------------------------------------ |
| **DOSR**      | 20      | 523          | **51.23%** | [config](./configs/pkinet/pkinet-s_dosr_ship.py) |
| **DOTA Ship** | 1       | 326          | **43.04%** | [config](./configs/pkinet/pkinet-s_dota_ship.py) |
| **LAFI**      | 49      | 5,120        | **26.79%** | [config](./configs/pkinet/pkinet-s_lafi_ship.py) |

### Detailed Results

#### 1. DOSR Dataset (20 ship classes)

- **Best mAP**: 51.23% at epoch 27
- **Training**: 523 images, 30 epochs
- **Validation**: 223 images
- **Model**: `work_dirs/pkinet-s_dosr_ship/epoch_30.pth`
- **Categories**: tanker, cargo, submarine, aircraft carrier, destroyer, etc.

#### 2. DOTA Ship Dataset (single class)

- **Best mAP**: 43.04% at epoch 27
- **Training**: 326 images with 28,068 ship instances
- **Validation**: 108 images with 8,960 ship instances
- **Model**: `work_dirs/pkinet-s_dota_ship/epoch_30.pth`
- **Category**: ship (generic)

#### 3. LAFI Dataset (49 fine-grained ship classes)

- **Best mAP**: 26.79% at epoch 6
- **Training**: 5,120 images
- **Validation**: 1,280 images
- **Model**: `work_dirs/pkinet-s_lafi_ship/epoch_8.pth`
- **Categories**: Nimitz, Enterprise, Arleigh_Burke_DD, Container_Ship, Ferry, Yacht, etc.

## Datasets

### Download Datasets and Models

**Baidu Netdisk Link**: [https://pan.baidu.com/s/5ZEE6OdCf9QEWK-0rm2I0qA](https://pan.baidu.com/s/5ZEE6OdCf9QEWK-0rm2I0qA)

The Baidu Netdisk share contains two folders:

#### 📁 Datasets Folder

Contains three ship detection datasets:

- `LAFI_dataset.tar.gz` (850MB) - 49 fine-grained ship categories, 5,120 train + 1,280 val images
- `dota_ship_only_dataset.tar.gz` (710MB) - Single ship class, 326 train + 108 val images
- `DOSR_converted_dataset.tar.gz` (585MB) - 20 ship types, 523 train + 223 val images

#### 📁 Models Folder

Contains pretrained weights and trained models:

- `pkinet_s_pretrain.pth` - ImageNet pretrained PKINet-S backbone
- `work_dirs/` - Trained models for all three datasets:
  - `pkinet-s_lafi_ship/` - Best mAP: 26.79% at epoch 6
  - `pkinet-s_dota_ship/` - Best mAP: 43.04% at epoch 27
  - `pkinet-s_dosr_ship/` - Best mAP: 51.23% at epoch 27

#### Installation Steps

1. Download datasets from Baidu Netdisk and extract to `data/` directory:

```bash
tar -xzf LAFI_dataset.tar.gz -C data/
tar -xzf dota_ship_only_dataset.tar.gz -C data/
tar -xzf DOSR_converted_dataset.tar.gz -C data/
```

2. Download pretrained backbone and place in `checkpoints/` directory:

```bash
mkdir -p checkpoints
# Move pkinet_s_pretrain.pth to checkpoints/
mv pkinet_s_pretrain.pth checkpoints/
```

3. (Optional) Download trained models and place in `work_dirs/`:

```bash
# Extract work_dirs folder from Baidu Netdisk
# This contains all trained model weights
```

### Dataset Details

### 1. LAFI Dataset

- **Location**: `data/LAFI/`
- **Training**: 5,120 images
- **Validation**: 1,280 images
- **Classes**: 49 fine-grained ship types (Nimitz, Enterprise, Perry_FF, Container_Ship, Cargo, Ferry, Yacht, etc.)

### 2. DOTA Ship-only Dataset

- **Location**: `data/dota_ship_only/`
- **Training**: 326 images, 28,068 ship instances
- **Validation**: 108 images, 8,960 ship instances
- **Classes**: 1 (ship)
- **Source**: Filtered from DOTA v1.0 dataset

### 3. DOSR Dataset

- **Location**: `data/DOSR_converted/`
- **Training**: 523 images
- **Validation**: 223 images
- **Classes**: 20 ship types (tanker, cargo, submarine, aircraft carrier, destroyer, etc.)
- **Format**: Converted from XML to DOTA format

## Installation

### Quick Install

We provide a quick installation script:

```bash
bash quick_install.sh
```

### Manual Installation

This project depends on [PyTorch](https://pytorch.org/), [MMCV](https://github.com/open-mmlab/mmcv), [MMDetection](https://github.com/open-mmlab/mmdetection), and [MMRotate](https://github.com/open-mmlab/mmrotate).

```bash
# Create conda environment
conda create --name pkinet python=3.8 -y
conda activate pkinet

# Install PyTorch
conda install pytorch==1.11.0 torchvision==0.12.0 cudatoolkit=11.3 -c pytorch

# Install dependencies
pip install yapf==0.40.1
pip install -U openmim
mim install mmcv-full
mim install mmdet
mim install mmengine

# Install this project
cd PKINet
mim install -v -e .
```

## Training

### Train All Datasets

Use the interactive training script:

```bash
bash train_all_datasets.sh
```

### Train Individual Dataset

```bash
# Train on DOSR dataset
python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py --work-dir work_dirs/pkinet-s_dosr_ship --gpu-ids 0

# Train on DOTA Ship dataset
python tools/train.py configs/pkinet/pkinet-s_dota_ship.py --work-dir work_dirs/pkinet-s_dota_ship --gpu-ids 0

# Train on LAFI dataset
python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py --work-dir work_dirs/pkinet-s_lafi_ship --gpu-ids 0
```

## Testing and Inference

### Test on Validation Set

```bash
python tools/test.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/epoch_30.pth \
    --eval mAP
```

### Visualize Results

```bash
python tools/test.py \
    configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/epoch_30.pth \
    --show-dir vis_results/
```

### Generate Predictions

Generate predictions for all three datasets:

```bash
bash generate_all_predictions.sh
```

## Project Structure

```
PKINet/
├── configs/pkinet/              # Training configs
│   ├── pkinet-s_lafi_ship.py
│   ├── pkinet-s_dota_ship.py
│   └── pkinet-s_dosr_ship.py
├── data/                        # Datasets
│   ├── LAFI/
│   ├── dota_ship_only/
│   └── DOSR_converted/
├── work_dirs/                   # Training outputs and models
├── tools/                       # Training and testing scripts
├── mmrotate/                    # Core framework code
├── checkpoints/                 # Pretrained backbone weights
├── README_TRAINING.md           # Detailed training guide
└── TRAINING_RESULTS.md          # Complete training logs
```

## Key Features

- **Multiple Datasets**: Trained on LAFI, DOTA Ship, and DOSR datasets
- **Rotated Bounding Boxes**: Precise ship orientation detection
- **Fine-grained Classification**: Up to 49 ship categories (LAFI)
- **High Performance**: Best mAP of 51.23% on DOSR dataset
- **Easy to Use**: Scripts for training, testing, and visualization
- **Pretrained Backbone**: ImageNet pretrained PKINet-S backbone

## Documentation

- **[Training Guide](README_TRAINING.md)**: Complete guide for setting up environment and training
- **[Training Results](TRAINING_RESULTS.md)**: Detailed training logs and performance analysis
- For MMRotate basics, see [official documentation](https://mmrotate.readthedocs.io/)

## License

This project is released under the [Apache 2.0 license](LICENSE).

## Acknowledgements

This project is based on:

- **PKINet**: [Poly Kernel Inception Network for Remote Sensing Detection (CVPR 2024)](https://openaccess.thecvf.com/content/CVPR2024/papers/Cai_Poly_Kernel_Inception_Network_for_Remote_Sensing_Detection_CVPR_2024_paper.pdf)
- **MMRotate**: [OpenMMLab Rotated Object Detection Toolbox](https://github.com/open-mmlab/mmrotate)
- **DOTA**: [A Large-scale Dataset for Object Detection in Aerial Images](https://captain-whu.github.io/DOTA/index.html)

## Citation

If you use this work or the trained models, please cite the original PKINet paper:

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

## Contact

For questions about this ship detection implementation, please open an issue in this repository.

For questions about the original PKINet method, please refer to the [original repository](https://github.com/caixiaoh/PKINet).
