from 方田_分数 import *

def 圭田术(广: 长度, 正从: 长度) -> 面积:
    return 广*分数(1, 2)*正从

def 邪田术(广一: 长度, 广二: 长度, 正从: 长度) -> 面积:
    return (广一+广二)*分数(1, 2)*正从

def 箕田术(舌广: 长度, 踵广: 长度, 正从: 长度):
    return (舌广+踵广)*分数(1, 2)*正从

def 圆田术(*, 周=长度(分数(0, 1), 分数(0, 1)), 径=长度(分数(0, 1), 分数(0, 1))) -> 面积:
    if 周==长度(分数(0, 1), 分数(0, 1)):
        return 径*径*分数(3, 4)
    elif 径==长度(分数(0, 1), 分数(0, 1)):
        return 周*周*分数(1, 12)
    else:
        return 周*径*分数(1, 4)

def 宛田术(周: 长度, 径: 长度) -> 面积:
    return 周*径*分数(1, 4)

def 弧田术(弦: 长度, 矢: 长度) -> 面积:
    return (弦*矢+矢*矢)*分数(1, 2)

def 环田术(中周: 长度, 外周: 长度, 径: 长度) -> 面积:
    return (中周+外周)*径*分数(1, 2)
