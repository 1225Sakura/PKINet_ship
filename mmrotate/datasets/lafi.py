# Copyright (c) OpenMMLab. All rights reserved.
from .builder import ROTATED_DATASETS
from .dota import DOTADataset


@ROTATED_DATASETS.register_module()
class LAFIDataset(DOTADataset):
    """LAFI船舶数据集，包含49个船舶类别."""

    CLASSES = ('AOE', 'Arleigh_Burke_DD', 'Asagiri_DD', 'Atago_DD',
               'Austin_LL', 'Barge', 'Cargo', 'Commander', 'Container_Ship',
               'Enterprise', 'EPF', 'Ferry', 'Fishing_Vessel', 'Hatsuyuki_DD',
               'Hovercraft', 'Hyuga_DD', 'LHA_LL', 'LSD_41_LL', 'Masyuu_AS',
               'Medical_Ship', 'Midway', 'Motorboat', 'Nimitz', 'Oil_Tanker',
               'Osumi_LL', 'Other_Aircraft_Carrier', 'Other_Auxiliary_Ship',
               'Other_Destroyer', 'Other_Frigate', 'Other_Landing',
               'Other_Merchant', 'Other_Ship', 'Other_Warship', 'Patrol',
               'Perry_FF', 'RoRo', 'Sailboat', 'Sanantonio_AS', 'Submarine',
               'Test_Ship', 'Ticonderoga', 'Training_Ship', 'Tugboat',
               'Wasp_LL', 'Yacht', 'YuDao_LL', 'YuDeng_LL', 'YuTing_LL',
               'YuZhao_LL')

    # 为每个类别生成一个颜色（49种颜色）
    PALETTE = [
        (165, 42, 42), (189, 183, 107),
        (0, 255, 0), (255, 0, 0), (138, 43, 226), (255, 128, 0), (255, 0, 255),
        (0, 255, 255), (255, 193, 193), (0, 51, 153), (255, 250, 205),
        (0, 139, 139), (255, 255, 0), (147, 116, 116), (0, 0, 255),
        (255, 165, 0), (0, 128, 0), (128, 0, 128), (255, 20, 147),
        (64, 224, 208), (255, 215, 0), (218, 165, 32), (123, 104, 238),
        (255, 105, 180), (0, 191, 255), (154, 205, 50), (255, 69, 0),
        (186, 85, 211), (100, 149, 237), (220, 20, 60), (72, 61, 139),
        (95, 158, 160), (244, 164, 96), (210, 105, 30), (144, 238, 144),
        (255, 182, 193), (176, 196, 222), (255, 222, 173), (0, 206, 209),
        (240, 128, 128), (135, 206, 250), (250, 128, 114), (173, 255, 47),
        (221, 160, 221), (238, 130, 238), (255, 160, 122), (32, 178, 170),
        (152, 251, 152), (255, 235, 205)
    ]
