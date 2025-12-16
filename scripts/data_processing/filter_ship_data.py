#!/usr/bin/env python3
"""筛选DOTA数据集中仅包含船舶（ship）类别的数据."""

import shutil
from pathlib import Path

from tqdm import tqdm


def filter_ship_from_dota(dota_base_dir,
                          output_dir,
                          split='train',
                          target_class='ship'):
    """从DOTA数据集中筛选指定类别的数据.

    Args:
        dota_base_dir: DOTA数据集根目录
        output_dir: 输出目录
        split: 数据集划分 (train/val)
        target_class: 目标类别名称
    """
    # 设置路径
    label_dir = Path(dota_base_dir) / split / 'labelTxt-v1.0'
    image_dir = Path(dota_base_dir) / split / 'images'

    output_label_dir = Path(output_dir) / split / 'annfiles'
    output_image_dir = Path(output_dir) / split / 'images'

    # 创建输出目录
    output_label_dir.mkdir(parents=True, exist_ok=True)
    output_image_dir.mkdir(parents=True, exist_ok=True)

    # 获取所有标注文件
    label_files = list(label_dir.glob('*.txt'))

    print(f'处理 {split} 集...')
    print(f'标注文件目录: {label_dir}')
    print(f'找到 {len(label_files)} 个标注文件')

    ship_count = 0
    file_count = 0

    for label_file in tqdm(label_files, desc=f'筛选{target_class}'):
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 前两行是元数据
        metadata = lines[:2]
        annotations = lines[2:]

        # 筛选包含目标类别的标注
        filtered_annotations = [
            line for line in annotations
            if line.strip() and target_class in line
        ]

        # 如果包含目标类别，保存文件
        if filtered_annotations:
            # 保存筛选后的标注文件
            output_label_file = output_label_dir / label_file.name
            with open(output_label_file, 'w', encoding='utf-8') as f:
                f.writelines(metadata)
                f.writelines(filtered_annotations)

            # 复制对应的图像文件
            image_name = label_file.stem + '.png'
            image_file = image_dir / image_name

            if image_file.exists():
                output_image_file = output_image_dir / image_name
                shutil.copy2(image_file, output_image_file)
                file_count += 1
                ship_count += len(filtered_annotations)
            else:
                print(f'警告: 图像文件不存在: {image_file}')

    print(f'{split} 集处理完成!')
    print(f'筛选出 {file_count} 个包含{target_class}的文件')
    print(f'共 {ship_count} 个{target_class}目标')
    print(f'输出目录: {output_dir}/{split}')

    return file_count, ship_count


def main():
    # DOTA数据集路径
    dota_base_dir = ('/home/user/dinov3/remote_sensing_segmentation/'
                     'datasets/DOTA')

    # 输出目录
    output_dir = '/home/user/PKINet/data/dota_ship_only'

    print('=' * 50)
    print('开始筛选DOTA数据集中的船舶数据')
    print('=' * 50)

    # 首先检查图像是否已解压
    train_image_dir = Path(dota_base_dir) / 'train' / 'images' / '1'
    if not train_image_dir.exists():
        print(f'\n错误: 训练集图像目录不存在: {train_image_dir}')
        print('请先解压图像文件!')

        # 尝试解压part1.zip
        part1_zip = Path(
            dota_base_dir) / 'train' / 'images' / '1' / 'part1.zip'
        parent_dir = part1_zip.parent
        if parent_dir.exists():
            print('\n正在解压训练集图像...')
            import zipfile

            # 找到所有zip文件
            zip_files = list(Path(dota_base_dir).rglob('part*.zip'))
            for zip_file in zip_files:
                if 'train/images' in str(zip_file):
                    print(f'解压: {zip_file}')
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(train_image_dir)

    # 处理训练集
    train_files, train_ships = filter_ship_from_dota(
        dota_base_dir, output_dir, split='train', target_class='ship')

    # 处理验证集
    val_files, val_ships = filter_ship_from_dota(
        dota_base_dir, output_dir, split='val', target_class='ship')

    print('\n' + '=' * 50)
    print('筛选完成!')
    print('=' * 50)
    print(f'训练集: {train_files} 个文件, {train_ships} 个船舶')
    print(f'验证集: {val_files} 个文件, {val_ships} 个船舶')
    print(f'总计: {train_files + val_files} 个文件, {train_ships + val_ships} 个船舶')
    print(f'\n输出目录: {output_dir}')


if __name__ == '__main__':
    main()
