# Copyright (c) OpenMMLab. All rights reserved.
from .builder import ROTATED_DATASETS
from .dota import DOTADataset


@ROTATED_DATASETS.register_module()
class DOTAShipDataset(DOTADataset):
    """DOTA数据集船舶类别，只包含1个类别: ship"""

    CLASSES = ('ship', )

    PALETTE = [(255, 0, 255)]
