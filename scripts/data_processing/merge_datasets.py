#!/usr/bin/env python3
"""合并LAFI和DOTA ship-only数据集."""

import shutil
from pathlib import Path

from tqdm import tqdm


def merge_datasets(lafi_dir, dota_ship_dir, output_dir):
    """合并LAFI和DOTA船舶数据集.

    Args:
        lafi_dir: LAFI数据集目录
        dota_ship_dir: DOTA ship-only数据集目录
        output_dir: 输出目录
    """
    for split in ['train', 'val']:
        print(f'\n处理 {split} 集...')

        # 创建输出目录
        output_annfiles = Path(output_dir) / split / 'annfiles'
        output_images = Path(output_dir) / split / 'images'
        output_annfiles.mkdir(parents=True, exist_ok=True)
        output_images.mkdir(parents=True, exist_ok=True)

        # 复制LAFI数据（使用png格式）
        lafi_ann_dir = Path(lafi_dir) / split / 'annotations'
        lafi_img_dir = Path(lafi_dir) / split / 'images'

        if lafi_ann_dir.exists():
            ann_files = list(lafi_ann_dir.glob('*.txt'))
            print(f'  复制LAFI {split} 数据: {len(ann_files)} 个文件...')

            for ann_file in tqdm(ann_files, desc=f'复制LAFI {split}'):
                # 复制标注文件，添加前缀避免冲突
                new_ann_name = f'lafi_{ann_file.name}'
                shutil.copy2(ann_file, output_annfiles / new_ann_name)

                # 复制图像文件（使用png格式）
                img_name = ann_file.stem + '.png'
                img_file = lafi_img_dir / img_name

                if img_file.exists():
                    new_img_name = f'lafi_{img_name}'
                    shutil.copy2(img_file, output_images / new_img_name)
                else:
                    print(f'    警告: 图像文件不存在: {img_file}')

        # 复制DOTA ship数据
        dota_ann_dir = Path(dota_ship_dir) / split / 'annfiles'
        dota_img_dir = Path(dota_ship_dir) / split / 'images'

        if dota_ann_dir.exists():
            ann_files = list(dota_ann_dir.glob('*.txt'))
            print(f'  复制DOTA ship {split} 数据: {len(ann_files)} 个文件...')

            for ann_file in tqdm(ann_files, desc=f'复制DOTA {split}'):
                # 复制标注文件，添加前缀避免冲突
                new_ann_name = f'dota_{ann_file.name}'
                shutil.copy2(ann_file, output_annfiles / new_ann_name)

                # 复制图像文件
                img_name = ann_file.stem + '.png'
                img_file = dota_img_dir / img_name

                if img_file.exists():
                    new_img_name = f'dota_{img_name}'
                    shutil.copy2(img_file, output_images / new_img_name)
                else:
                    print(f'    警告: 图像文件不存在: {img_file}')

        # 统计结果
        total_ann = len(list(output_annfiles.glob('*.txt')))
        total_img = len(list(output_images.glob('*.png')))
        print(f'  {split} 集合并完成: {total_ann} 个标注, {total_img} 个图像')


def main():
    # 数据集路径
    lafi_dir = '/home/user/PKINet/data/LAFI'
    dota_ship_dir = '/home/user/PKINet/data/dota_ship_only'
    output_dir = '/home/user/PKINet/data/combined_ship_dataset'

    print('=' * 60)
    print('合并LAFI和DOTA ship-only数据集')
    print('=' * 60)

    merge_datasets(lafi_dir, dota_ship_dir, output_dir)

    print('\n' + '=' * 60)
    print('合并完成!')
    print('=' * 60)
    print(f'输出目录: {output_dir}')

    # 最终统计
    train_ann = len(list(Path(output_dir).glob('train/annfiles/*.txt')))
    train_img = len(list(Path(output_dir).glob('train/images/*.png')))
    val_ann = len(list(Path(output_dir).glob('val/annfiles/*.txt')))
    val_img = len(list(Path(output_dir).glob('val/images/*.png')))

    print('\n最终统计:')
    print(f'  训练集: {train_ann} 个标注, {train_img} 个图像')
    print(f'  验证集: {val_ann} 个标注, {val_img} 个图像')
    print(f'  总计: {train_ann + val_ann} 个标注, {train_img + val_img} 个图像')


if __name__ == '__main__':
    main()
