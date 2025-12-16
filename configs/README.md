# PKINet Ship Detection Configurations

This directory contains training configurations for ship detection using PKINet.

## Active Configurations

### Ship Detection Configs (in `pkinet/` directory)

1. **pkinet-s_lafi_ship.py**

   - Dataset: LAFI
   - Classes: 49 fine-grained ship types
   - Best mAP: 26.79%
   - Model: `work_dirs/pkinet-s_lafi_ship/epoch_8.pth`

2. **pkinet-s_dota_ship.py**

   - Dataset: DOTA Ship-only
   - Classes: 1 (ship)
   - Best mAP: 43.04%
   - Model: `work_dirs/pkinet-s_dota_ship/epoch_30.pth`

3. **pkinet-s_dosr_ship.py**

   - Dataset: DOSR
   - Classes: 20 ship types
   - Best mAP: 51.23%
   - Model: `work_dirs/pkinet-s_dosr_ship/epoch_30.pth`

## Usage

### Training

```bash
# Train on DOSR dataset (best performance)
python tools/train.py configs/pkinet/pkinet-s_dosr_ship.py --work-dir work_dirs/pkinet-s_dosr_ship --gpu-ids 0

# Train on DOTA Ship dataset
python tools/train.py configs/pkinet/pkinet-s_dota_ship.py --work-dir work_dirs/pkinet-s_dota_ship --gpu-ids 0

# Train on LAFI dataset
python tools/train.py configs/pkinet/pkinet-s_lafi_ship.py --work-dir work_dirs/pkinet-s_lafi_ship --gpu-ids 0
```

### Testing

```bash
# Test and evaluate
python tools/test.py configs/pkinet/pkinet-s_dosr_ship.py work_dirs/pkinet-s_dosr_ship/epoch_30.pth --eval mAP

# Test with visualization
python tools/test.py configs/pkinet/pkinet-s_dosr_ship.py work_dirs/pkinet-s_dosr_ship/epoch_30.pth --show-dir vis_results/
```

## Configuration Parameters

All ship detection configs use:

- **Backbone**: PKINet-S (pretrained on ImageNet)
- **Neck**: FPN
- **Head**: Oriented R-CNN
- **Optimizer**: AdamW (lr=0.0002, weight_decay=0.05)
- **Batch Size**: 2 per GPU
- **Image Size**: 1024×1024
- **Training Epochs**: 30
- **Validation Interval**: Every 3 epochs

## Other Configs

Other model configurations in this directory are part of the original MMRotate framework and have been preserved for reference. They are not actively used in this ship detection project.

To explore other MMRotate models, see:

- [MMRotate Model Zoo](https://mmrotate.readthedocs.io/en/latest/model_zoo.html)
- Other config directories (cfa, convnext, oriented_rcnn, etc.)

## Documentation

- [Main README](../README.md) - Project overview
- [Training Guide](../README_TRAINING.md) - Complete training instructions
- [Training Results](../TRAINING_RESULTS.md) - Detailed performance analysis
