#!/usr/bin/env python
"""可视化三个数据集的预测结果."""
import os
import random

import mmcv
from mmdet.apis import inference_detector, init_detector


def visualize_dataset(config_file,
                      checkpoint_file,
                      data_root,
                      img_prefix,
                      output_dir,
                      num_samples=10):
    """可视化数据集的预测结果.

    Args:
        config_file: 配置文件路径
        checkpoint_file: 模型checkpoint路径
        data_root: 数据根目录
        img_prefix: 图像目录
        output_dir: 输出目录
        num_samples: 可视化样本数量
    """
    # 初始化模型
    model = init_detector(config_file, checkpoint_file, device='cuda:0')

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有图像文件
    img_files = [f for f in os.listdir(img_prefix) if f.endswith('.png')]

    # 随机选择样本
    sample_files = random.sample(img_files, min(num_samples, len(img_files)))

    print(f'处理 {len(sample_files)} 张图像...')

    for idx, img_file in enumerate(sample_files):
        img_path = os.path.join(img_prefix, img_file)

        # 推理
        result = inference_detector(model, img_path)

        # 可视化
        img = mmcv.imread(img_path)

        # 可视化检测结果
        out_file = os.path.join(output_dir, f'result_{idx:03d}_{img_file}')
        model.show_result(img, result, score_thr=0.3, out_file=out_file)

        print(f'  [{idx+1}/{len(sample_files)}] 保存结果到: {out_file}')

    print(f'完成! 结果保存在: {output_dir}')


if __name__ == '__main__':
    # 配置
    datasets = {
        'LAFI': {
            'config': 'configs/pkinet/pkinet-s_lafi_ship.py',
            'checkpoint': 'work_dirs/pkinet-s_lafi_ship/latest.pth',
            'img_prefix': 'data/LAFI/val/images',
            'output_dir': 'work_dirs/vis_results/lafi'
        },
        'DOTA_Ship': {
            'config': 'configs/pkinet/pkinet-s_dota_ship.py',
            'checkpoint': 'work_dirs/pkinet-s_dota_ship/latest.pth',
            'img_prefix': 'data/dota_ship_only/val/images',
            'output_dir': 'work_dirs/vis_results/dota_ship'
        },
        'DOSR': {
            'config': 'configs/pkinet/pkinet-s_dosr_ship.py',
            'checkpoint': 'work_dirs/pkinet-s_dosr_ship/latest.pth',
            'img_prefix': 'data/DOSR_converted/val/images',
            'output_dir': 'work_dirs/vis_results/dosr'
        }
    }

    # 处理每个数据集
    for dataset_name, config in datasets.items():
        print(f"\n{'='*60}")
        print(f'可视化 {dataset_name} 数据集')
        print(f"{'='*60}")

        if not os.path.exists(config['checkpoint']):
            print(f"警告: checkpoint不存在 {config['checkpoint']}")
            continue

        try:
            visualize_dataset(
                config['config'],
                config['checkpoint'],
                None,
                config['img_prefix'],
                config['output_dir'],
                num_samples=10)
        except Exception as e:
            print(f'错误: {e}')
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print('所有数据集可视化完成!')
    print(f"{'='*60}")
