#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2024-03-22
"""
import cv2
from visioncube.measure import ColorMeasurement


img_path = 'data/test-150.jpg'
img = cv2.imread(img_path)
points = [[50, 50], [60, 50], [60, 60], [50, 60]]
res = ColorMeasurement(points)({"image": img})['color_measure']
print(res)