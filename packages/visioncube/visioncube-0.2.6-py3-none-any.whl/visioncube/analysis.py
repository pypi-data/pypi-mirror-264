#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2024-02-28
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

from more_itertools import windowed

"""
1. 直方图
    (1). 亮度均匀：说明图像的对比度较低。[对比度, 直方图均衡化, 自适应直方图均衡化]
    (2). 有明显峰值：说明图像中存在某些特定的颜色或亮度值
    (3). 有离散的灰度值：说明图像可能存在椒盐噪声。[中值滤波]
"""


class AnalysisHistogram:

    def __init__(self, img_path):
        self.size = 256
        self.hist = self.get_histogram(img_path)

    def get_histogram(self, img_path):
        image = cv2.imread(img_path, 0)
        # images, channels, mask, histSize, ranges
        hist = cv2.calcHist([image], [0], None, [self.size], [0, self.size])

        return hist

    def is_uniform(self):
        """
        判断直方图是否均匀
        直方图的标准差小: 亮度之间的差异小，亮度分布越均匀
        直方图的标准差大: 亮度之间的差异大

        不均匀，则需要调整
        """
        frequency = self.hist / self.hist.sum()
        chunk_sum = np.array(np.split(frequency, 4)).sum(axis=1)
        # print(chunk_sum)

        # 计算频率的标准差
        std_dev = np.std(chunk_sum)
        if std_dev > 0.1:
            print('not uniform')
        else:
            print('uniform')

    def is_dark(self):
        """图像是否过暗"""
        frequency = self.hist / self.hist.sum()
        chunk_arr = np.split(frequency, 4)
        if chunk_arr[0].sum() >= 0.5:
            print('too dark')

    def is_bright(self):
        """图像是否过亮"""
        frequency = self.hist / self.hist.sum()
        chunk_arr = np.split(frequency, 4)
        if chunk_arr[-1].sum() >= 0.5:
            print('too bright')

    def draw_hist(self):
        plt.plot(self.hist, color='gray')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        plt.show()

    def __call__(self):
        self.is_uniform()
        self.is_dark()
        self.is_bright()

        print()


if __name__ == '__main__':
    print("<=============== 过暗图像 ===============>")
    img_path = '../data/analysis1.png'
    analyzer = AnalysisHistogram(img_path)
    analyzer()
    # analyzer.draw_hist()

    print('<=============== 正常图像 ===============>')
    img_path = '../data/analysis1-1.png'
    analyzer = AnalysisHistogram(img_path)
    analyzer()
    # analyzer.draw_hist()

    print('<=============== 过亮图像 ===============>')
    img_path = '../data/analysis1-2.png'
    analyzer = AnalysisHistogram(img_path)
    analyzer()
    # analyzer.draw_hist()

    print('<=============== 其他图像 ===============>')
    img_path = '../data/lena.jpeg'
    analyzer = AnalysisHistogram(img_path)
    analyzer()
    analyzer.draw_hist()
