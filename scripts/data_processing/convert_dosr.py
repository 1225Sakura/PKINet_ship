#!/usr/bin/env python3
"""将DOSR数据集的XML标注转换为DOTA格式的txt文件."""

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from tqdm import tqdm


def convert_xml_to_dota(xml_file):
    """将DOSR的XML标注转换为DOTA格式.

    Args:
        xml_file: XML文件路径

    Returns:
        list: DOTA格式的标注行列表
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    annotations = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        difficult = obj.find('difficult').text

        bndbox = obj.find('bndbox')
        x1 = bndbox.find('x1').text
        y1 = bndbox.find('y1').text
        x2 = bndbox.find('x2').text
        y2 = bndbox.find('y2').text
        x3 = bndbox.find('x3').text
        y3 = bndbox.find('y3').text
        x4 = bndbox.find('x4').text
        y4 = bndbox.find('y4').text

        # DOTA格式: x1 y1 x2 y2 x3 y3 x4 y4 class_name difficulty
        line = f'{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} {name} {difficult}\n'
        annotations.append(line)

    return annotations


def convert_dosr_dataset(dosr_dir, output_dir):
    """转换DOSR数据集.

    Args:
        dosr_dir: DOSR数据集目录
        output_dir: 输出目录
    """
    dosr_dir = Path(dosr_dir)
    output_dir = Path(output_dir)

    # 读取数据集划分
    splits = ['train', 'val']

    for split in splits:
        print(f'\n处理 {split} 集...')

        # 创建输出目录
        output_annfiles = output_dir / split / 'annfiles'
        output_images = output_dir / split / 'images'
        output_annfiles.mkdir(parents=True, exist_ok=True)
        output_images.mkdir(parents=True, exist_ok=True)

        # 读取文件列表
        split_file = dosr_dir / 'ImageSets' / f'{split}.txt'
        with open(split_file, 'r') as f:
            file_names = [line.strip() for line in f.readlines()]

        print(f'  找到 {len(file_names)} 个文件')

        # 转换每个文件
        for file_name in tqdm(file_names, desc=f'转换{split}'):
            # 转换XML到txt
            xml_file = (
                dosr_dir / 'Annotations_8_parameters_version' /
                f'{file_name}.xml')

            if not xml_file.exists():
                print(f'  警告: {xml_file} 不存在')
                continue

            annotations = convert_xml_to_dota(xml_file)

            # 添加元数据
            metadata = ['imagesource:DOSR\n', 'gsd:0.5\n']

            # 保存txt文件
            txt_file = output_annfiles / f'{file_name}.txt'
            with open(txt_file, 'w') as f:
                f.writelines(metadata)
                f.writelines(annotations)

            # 复制图像
            img_file = dosr_dir / 'Images' / f'{file_name}.png'
            if img_file.exists():
                shutil.copy2(img_file, output_images / f'{file_name}.png')
            else:
                print(f'  警告: {img_file} 不存在')

        # 统计结果
        total_ann = len(list(output_annfiles.glob('*.txt')))
        total_img = len(list(output_images.glob('*.png')))
        print(f'  {split} 集完成: {total_ann} 个标注, {total_img} 个图像')


def main():
    dosr_dir = '/home/user/PKINet/data/DOSR'
    output_dir = '/home/user/PKINet/data/DOSR_converted'

    print('=' * 60)
    print('转换DOSR数据集为DOTA格式')
    print('=' * 60)

    convert_dosr_dataset(dosr_dir, output_dir)

    print('\n' + '=' * 60)
    print('转换完成!')
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


if __name__ == '__main__':
    main()
