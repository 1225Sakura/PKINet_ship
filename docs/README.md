# Documentation

This repository focuses on ship detection using PKINet. For detailed documentation, please refer to:

## Main Documentation

- **[README.md](../README.md)** - Project overview and quick start guide
- **[README_zh-CN.md](../README_zh-CN.md)** - Chinese version of project overview
- **[README_TRAINING.md](../README_TRAINING.md)** - Complete training guide
- **[TRAINING_RESULTS.md](../TRAINING_RESULTS.md)** - Detailed training results and analysis

## Configuration Files

All training configurations are in `configs/pkinet/`:

- `pkinet-s_lafi_ship.py` - LAFI dataset (49 ship classes)
- `pkinet-s_dota_ship.py` - DOTA Ship dataset (1 class)
- `pkinet-s_dosr_ship.py` - DOSR dataset (20 ship classes)

## MMRotate Framework Documentation

For detailed documentation about the underlying MMRotate framework, please visit:

- [MMRotate Official Documentation](https://mmrotate.readthedocs.io/)
- Original MMRotate documentation (backup): `docs_mmrotate_backup/`

## Quick Links

### Installation

```bash
bash quick_install.sh
```

### Training

```bash
# Train all datasets
bash train_all_datasets.sh

# Or train individual dataset
python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py --work-dir work_dirs/pkinet-s_dosr_ship --gpu-ids 0
```

### Testing

```bash
python tools/test.py configs/pkinet/pkinet-s_dosr_ship.py work_dirs/pkinet-s_dosr_ship/epoch_30.pth --eval mAP
```

## Contact

For questions about this ship detection implementation, please open an issue in this repository.
