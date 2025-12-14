# PKINet 船舶检测训练结果报告

**训练日期**: 2025-12-06 ~ 2025-12-07
**预训练模型**: checkpoints/pkinet_s_pretrain.pth
**训练框架**: MMRotate + PyTorch 1.11.0

---

## 📊 精度汇总

### 1. LAFI数据集 (49个船舶类别)

**数据集信息**:
- 训练样本: 5,120张图像
- 验证样本: 1,280张图像
- 类别数: 49 (包括Nimitz, Enterprise, Perry_FF等)

**训练结果**:
| Epoch | mAP   | 说明           |
|-------|-------|----------------|
| 3     | 0.146 | 早期验证       |
| 6     | 0.268 | 最佳结果       |

- **最佳mAP**: **26.79%** (Epoch 6)
- **状态**: 提前停止 (训练至Epoch 8)
- **模型路径**: `work_dirs/pkinet-s_lafi_ship/epoch_8.pth`
- **配置文件**: `configs/pkinet/pkinet-s_lafi_ship.py`

---

### 2. DOTA Ship数据集 (1个类别: ship)

**数据集信息**:
- 训练样本: 326张图像 (28,068个船舶实例)
- 验证样本: 108张图像 (8,960个船舶实例)
- 类别数: 1 (ship)

**训练结果**:
| Epoch | mAP   | 提升    |
|-------|-------|---------|
| 3     | 0.195 | -       |
| 6     | 0.359 | +16.4%  |
| 9     | 0.397 | +3.8%   |
| 12    | 0.411 | +1.4%   |
| 15    | 0.415 | +0.3%   |
| 18    | 0.425 | +1.0%   |
| 21    | 0.430 | +0.4%   |
| 24    | 0.429 | -0.1%   |
| 27    | 0.430 | +0.1%   |
| 30    | 0.429 | -0.1%   |

- **最佳mAP**: **43.04%** (Epoch 27)
- **状态**: 完整训练30个epoch
- **模型路径**: `work_dirs/pkinet-s_dota_ship/epoch_30.pth`
- **配置文件**: `configs/pkinet/pkinet-s_dota_ship.py`

---

### 3. DOSR数据集 (20个船舶类别)

**数据集信息**:
- 训练样本: 523张图像
- 验证样本: 223张图像
- 类别数: 20 (包括tanker, cargo, submarine等)

**训练结果**:
| Epoch | mAP   | 提升    |
|-------|-------|---------|
| 3     | 0.092 | -       |
| 6     | 0.207 | +11.5%  |
| 9     | 0.307 | +10.0%  |
| 12    | 0.390 | +8.3%   |
| 15    | 0.393 | +0.2%   |
| 18    | 0.461 | +6.9%   |
| 21    | 0.494 | +3.2%   |
| 24    | 0.501 | +0.7%   |
| 27    | 0.512 | +1.1%   |
| 30    | 0.505 | -0.7%   |

- **最佳mAP**: **51.23%** (Epoch 27)
- **状态**: 完整训练30个epoch
- **模型路径**: `work_dirs/pkinet-s_dosr_ship/epoch_30.pth`
- **配置文件**: `configs/pkinet/pkinet-s_dosr_ship.py`

---

## 🎯 性能对比

| 数据集      | 类别数 | 训练样本 | 最佳mAP | 最佳Epoch | 收敛状态     |
|-------------|--------|----------|---------|-----------|--------------|
| LAFI        | 49     | 5,120    | 26.79%  | 6         | 提前停止     |
| DOTA Ship   | 1      | 326      | 43.04%  | 27        | 已收敛       |
| DOSR        | 20     | 523      | 51.23%  | 30        | 接近收敛     |

**关键发现**:
1. **DOSR表现最佳** (51.23% mAP) - 尽管类别数较多(20类)，但数据质量好
2. **DOTA Ship次之** (43.04% mAP) - 单类别检测，精度稳定
3. **LAFI最具挑战** (26.79% mAP) - 49个细粒度类别，需要更长时间训练

---

## 📁 可视化结果

### 预测结果图像位置:

1. **LAFI数据集**: `work_dirs/vis_results/lafi/`
   - 包含10张示例预测结果
   - 文件名: `result_000_*.png` ~ `result_009_*.png`

2. **DOTA Ship数据集**: `work_dirs/vis_results/dota_ship/`
   - 包含10张示例预测结果
   - 文件名: `result_000_P*.png` ~ `result_009_P*.png`

3. **DOSR数据集**: `work_dirs/vis_results/dosr/`
   - 包含10张示例预测结果
   - 文件名: `result_000_*.png` ~ `result_009_*.png`

---

## 🔧 训练配置

### 通用配置:
- **Backbone**: PKINet-S (预训练)
- **Neck**: FPN
- **Head**: Oriented R-CNN
- **优化器**: AdamW (lr=0.0002, weight_decay=0.05)
- **Batch Size**: 2 per GPU
- **学习率策略**: Step decay (warmup 500 iters)
- **数据增强**: RResize, RRandomFlip (horizontal, vertical, diagonal)
- **图像尺寸**: 1024×1024

### 硬件配置:
- **GPU**: 4× NVIDIA GeForce RTX 4090
- **CUDA**: 11.3
- **训练模式**: 单GPU训练 (gpu_ids=[0])

---

## 📝 使用说明

### 查看预测结果:
```bash
# 查看LAFI结果
ls work_dirs/vis_results/lafi/

# 查看DOTA Ship结果
ls work_dirs/vis_results/dota_ship/

# 查看DOSR结果
ls work_dirs/vis_results/dosr/
```

### 测试新图像:
```bash
# 使用训练好的模型进行推理
python tools/test.py configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/latest.pth \
    --show-dir test_results/
```

### 继续训练:
```bash
# 如果需要继续训练LAFI (从epoch 8继续)
python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py \
    --resume-from work_dirs/pkinet-s_lafi_ship/latest.pth \
    --gpu-ids 0
```

---

## 🎓 结论与建议

1. **DOSR数据集**表现出色，建议:
   - 模型已基本收敛，可直接用于实际应用
   - 可尝试更大的backbone (PKINet-M/L) 进一步提升性能

2. **DOTA Ship数据集**已完全收敛:
   - 单类别检测精度良好
   - 适合作为通用船舶检测baseline

3. **LAFI数据集**需要改进:
   - 49个细粒度类别较为困难
   - 建议延长训练至30个epoch
   - 可考虑使用类别平衡策略或focal loss

---

**生成时间**: 2025-12-07
**报告版本**: v1.0
