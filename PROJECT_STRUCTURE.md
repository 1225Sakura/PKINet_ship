# PKINet 项目结构说明

## 📁 核心目录

### 主要代码

```
PKINet/
├── mmrotate/              # 核心框架代码
├── configs/               # 训练配置文件
│   ├── pkinet/           # 船舶检测配置
│   └── _base_/           # 基础配置
├── tools/                 # 训练和测试工具
└── tests/                 # 测试代码
```

### 数据和模型

```
├── data/                  # 数据集 (18GB, 已在.gitignore)
│   ├── LAFI/
│   ├── dota_ship_only/
│   └── DOSR_converted/
├── checkpoints/           # 预训练模型 (89MB, 已在.gitignore)
├── work_dirs/             # 训练输出 (3.4GB, 已在.gitignore)
│   ├── pkinet-s_lafi_ship/
│   ├── pkinet-s_dota_ship/
│   └── pkinet-s_dosr_ship/
└── datasets_archives/     # 数据集压缩包 (10.7GB, 已在.gitignore)
    ├── LAFI_dataset.tar.gz
    ├── dota_ship_only_dataset.tar.gz
    └── DOSR_converted_dataset.tar.gz
```

### 脚本和工具

```
├── scripts/
│   ├── training/          # 训练脚本
│   │   ├── train_all_datasets.sh
│   │   ├── train_ships.sh
│   │   ├── start_training.sh
│   │   ├── test_train.sh
│   │   └── generate_all_predictions.sh
│   ├── data_processing/   # 数据处理脚本
│   │   ├── convert_dosr.py
│   │   ├── filter_ship_data.py
│   │   ├── merge_datasets.py
│   │   ├── unify_annotations.py
│   │   └── visualize_results.py
│   ├── quick_install.sh   # 快速安装
│   └── install_deps_existing_env.sh
```

### 文档

```
├── README.md              # 项目主文档 (英文)
├── README_zh-CN.md        # 项目主文档 (中文)
├── README_TRAINING.md     # 训练指南
├── TRAINING_RESULTS.md    # 训练结果
├── docs/
│   ├── README.md          # 文档索引
│   ├── archived/          # 备份文档
│   │   ├── MMRotate_README.md.backup
│   │   └── MMRotate_README_zh-CN.md.backup
│   └── mmrotate_original/ # 原始MMRotate文档
```

______________________________________________________________________

## 🗑️ 已清理的内容

### 删除的文件

- ✅ `*.log` - 日志文件
- ✅ `PUSH_INSTRUCTIONS.md` - 临时推送说明
- ✅ `FINAL_PUSH_SOLUTION.md` - 临时解决方案文档

### 移动的文件

- ✅ 所有训练脚本 → `scripts/training/`
- ✅ 所有数据处理脚本 → `scripts/data_processing/`
- ✅ 安装脚本 → `scripts/`
- ✅ 数据集压缩包 → `datasets_archives/`
- ✅ 备份文档 → `docs/archived/` 和 `docs/mmrotate_original/`

### 清理的内容

- ✅ work_dirs: 5.9GB → 3.4GB (删除中间checkpoint和日志)
  - 保留: `best_mAP_*.pth`, `epoch_30.pth`, `epoch_27.pth`
  - 删除: 中间epoch模型, 训练日志

______________________________________________________________________

## 📊 磁盘使用统计

| 目录               | 大小      | 说明               |
| ------------------ | --------- | ------------------ |
| data/              | 18GB      | 原始数据集         |
| datasets_archives/ | 10.7GB    | 压缩的数据集       |
| work_dirs/         | 3.4GB     | 训练输出（已清理） |
| checkpoints/       | 89MB      | 预训练模型         |
| **总计**           | **~32GB** |                    |

______________________________________________________________________

## 🔧 常用命令

### 训练

```bash
# 训练所有数据集
bash scripts/training/train_all_datasets.sh

# 训练单个数据集
python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py \
    --work-dir work_dirs/pkinet-s_dosr_ship --gpu-ids 0
```

### 测试

```bash
# 测试模型
python tools/test.py configs/pkinet/pkinet-s_dosr_ship.py \
    work_dirs/pkinet-s_dosr_ship/best_mAP_epoch_27.pth --eval mAP
```

### 数据处理

```bash
# 转换DOSR数据集
python scripts/data_processing/convert_dosr.py

# 筛选船舶数据
python scripts/data_processing/filter_ship_data.py
```

______________________________________________________________________

## 📝 注意事项

1. **大文件**: `data/`, `checkpoints/`, `work_dirs/`, `datasets_archives/` 已在.gitignore中
2. **数据集下载**: 见README.md中的百度网盘链接
3. **模型位置**: 训练好的模型在 `work_dirs/pkinet-s_*/best_mAP_*.pth`

______________________________________________________________________

**最后更新**: 2025-12-13
**项目版本**: 船舶检测专用版本
