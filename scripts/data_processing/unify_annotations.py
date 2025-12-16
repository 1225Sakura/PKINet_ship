#!/usr/bin/env python3
"""
统一LAFI和DOTA数据集的标注格式
1. 为LAFI标注文件添加元数据行
2. 统计所有船舶类别
"""

from collections import Counter
from pathlib import Path

from tqdm import tqdm


def analyze_and_unify(dataset_dir):
    """分析并统一标注格式.

    Args:
        dataset_dir: 数据集目录
    """
    # 统计所有类别
    all_classes = Counter()

    for split in ['train', 'val']:
        annfiles_dir = Path(dataset_dir) / split / 'annfiles'

        if not annfiles_dir.exists():
            continue

        ann_files = list(annfiles_dir.glob('*.txt'))
        print(f'\n处理 {split} 集: {len(ann_files)} 个文件')

        for ann_file in tqdm(ann_files, desc=f'分析{split}'):
            with open(ann_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 检查是否有元数据行
            has_metadata = False
            if lines and 'imagesource' in lines[0].lower():
                has_metadata = True
                annotations = lines[2:]
            else:
                annotations = lines

            # 统计类别
            for line in annotations:
                parts = line.strip().split()
                if len(parts) >= 9:
                    class_name = parts[8]
                    all_classes[class_name] += 1

            # 如果没有元数据，添加元数据
            if not has_metadata and annotations:
                metadata = ['imagesource:combined\n', 'gsd:0.5\n']
                with open(ann_file, 'w', encoding='utf-8') as f:
                    f.writelines(metadata)
                    f.writelines(annotations)

    return all_classes


def unify_to_ship_class(dataset_dir):
    """将所有类别统一为 'ship'.

    Args:
        dataset_dir: 数据集目录
    """
    for split in ['train', 'val']:
        annfiles_dir = Path(dataset_dir) / split / 'annfiles'

        if not annfiles_dir.exists():
            continue

        ann_files = list(annfiles_dir.glob('*.txt'))
        print(f"\n统一 {split} 集类别为 'ship': {len(ann_files)} 个文件")

        for ann_file in tqdm(ann_files, desc=f'统一{split}'):
            with open(ann_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 确保有元数据
            if lines and 'imagesource' in lines[0].lower():
                metadata = lines[:2]
                annotations = lines[2:]
            else:
                metadata = ['imagesource:combined\n', 'gsd:0.5\n']
                annotations = lines

            # 统一类别为 ship
            new_annotations = []
            for line in annotations:
                parts = line.strip().split()
                if len(parts) >= 9:
                    # 替换类别名
                    parts[8] = 'ship'
                    new_annotations.append(' '.join(parts) + '\n')

            # 写回文件
            with open(ann_file, 'w', encoding='utf-8') as f:
                f.writelines(metadata)
                f.writelines(new_annotations)


def main():
    dataset_dir = '/home/user/PKINet/data/combined_ship_dataset'

    print('=' * 60)
    print('分析数据集类别')
    print('=' * 60)

    # 分析类别
    all_classes = analyze_and_unify(dataset_dir)

    print('\n' + '=' * 60)
    print('类别统计:')
    print('=' * 60)
    for class_name, count in sorted(
            all_classes.items(), key=lambda x: x[1], reverse=True):
        print(f'  {class_name}: {count}')

    print(f'\n总类别数: {len(all_classes)}')

    # 询问是否统一为ship类别
    print('\n' + '=' * 60)
    print("统一所有类别为 'ship'")
    print('=' * 60)

    # 直接统一为ship
    unify_to_ship_class(dataset_dir)

    print('\n' + '=' * 60)
    print('完成!')
    print('=' * 60)
    print("所有标注已统一为 'ship' 类别")


if __name__ == '__main__':
    main()
