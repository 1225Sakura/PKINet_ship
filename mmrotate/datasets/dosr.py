# Copyright (c) OpenMMLab. All rights reserved.
import glob
import os.path as osp

import numpy as np

from mmrotate.core import poly2obb_np
from .builder import ROTATED_DATASETS
from .dota import DOTADataset


@ROTATED_DATASETS.register_module()
class DOSRDataset(DOTADataset):
    """DOSR船舶数据集，包含20个船舶类别."""

    CLASSES = ('auxiliary ship', 'barge', 'bulk cargo vessel', 'cargo',
               'communication ship', 'container', 'cruise', 'deckbarge',
               'deckship', 'fishing boat', 'flat traffic ship',
               'floating crane', 'military_ship', 'multihull', 'speedboat',
               'submarine', 'tanker', 'transpot', 'tug', 'yacht')

    PALETTE = [(165, 42, 42), (189, 183, 107), (0, 255, 0), (255, 0, 0),
               (138, 43, 226), (255, 128, 0), (255, 0, 255), (0, 255, 255),
               (255, 193, 193), (0, 51, 153), (255, 250, 205), (0, 139, 139),
               (255, 255, 0), (147, 116, 116), (0, 0, 255), (255, 165, 0),
               (0, 128, 0), (128, 0, 128), (255, 20, 147), (64, 224, 208)]

    def load_annotations(self, ann_folder):
        """重写以处理包含空格的类别名称."""
        cls_map = {c: i for i, c in enumerate(self.CLASSES)}
        ann_files = glob.glob(ann_folder + '/*.txt')
        data_infos = []
        if not ann_files:
            ann_files = glob.glob(ann_folder + '/*/*.txt')

        for ann_file in ann_files:
            data_info = {}
            img_id = osp.split(ann_file)[1][:-4]
            img_name = img_id + '.png'
            data_info['filename'] = img_name
            data_info['ann'] = {}
            gt_bboxes = []
            gt_labels = []
            gt_polygons = []
            gt_bboxes_ignore = []
            gt_labels_ignore = []
            gt_polygons_ignore = []

            if osp.getsize(ann_file) == 0 and self.filter_empty_gt:
                continue

            with open(ann_file) as f:
                s = f.readlines()
                for si in s:
                    bbox_info = si.split()
                    poly = np.array(bbox_info[:8], dtype=np.float32)
                    try:
                        x, y, w, h, a = poly2obb_np(poly, self.version)
                    except Exception:  # noqa: E722
                        continue
                    # difficulty is always the last field
                    difficulty = int(bbox_info[-1])
                    # class name is from index 8 to second-last field
                    cls_name = ' '.join(bbox_info[8:-1])

                    if cls_name not in cls_map:
                        continue

                    label = cls_map[cls_name]
                    if difficulty > self.difficulty:
                        pass
                    else:
                        gt_bboxes.append([x, y, w, h, a])
                        gt_labels.append(label)
                        gt_polygons.append(poly)

            if gt_bboxes:
                data_info['ann']['bboxes'] = np.array(
                    gt_bboxes, dtype=np.float32)
                data_info['ann']['labels'] = np.array(
                    gt_labels, dtype=np.int64)
                data_info['ann']['polygons'] = np.array(
                    gt_polygons, dtype=np.float32)
            else:
                data_info['ann']['bboxes'] = np.zeros((0, 5), dtype=np.float32)
                data_info['ann']['labels'] = np.array([], dtype=np.int64)
                data_info['ann']['polygons'] = np.zeros((0, 8),
                                                        dtype=np.float32)

            if gt_polygons_ignore:
                data_info['ann']['bboxes_ignore'] = np.array(
                    gt_bboxes_ignore, dtype=np.float32)
                data_info['ann']['labels_ignore'] = np.array(
                    gt_labels_ignore, dtype=np.int64)
                data_info['ann']['polygons_ignore'] = np.array(
                    gt_polygons_ignore, dtype=np.float32)

            data_infos.append(data_info)

        self.img_ids = [*map(lambda x: x['filename'][:-4], data_infos)]
        return data_infos
