#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2024-03-14
"""
import os
import random
import shutil
from copy import deepcopy

import cv2
import numpy as np

from visioncube import read_image, rgb_to_bgr
from importlib import import_module

operator_name = 'AdditiveGaussianNoise'


def get_param(min_n, max_n):
    param = np.random.uniform(min_n, max_n, size=8)
    boundary = np.array([min_n, max_n])
    return np.append(param, boundary)


def pipeline_test(img_path=None):
    device = 'cuda'

    img_path = 'data/anomaly.jpg'
    image = read_image(img_path)
    doc = {'image': image}

    impl = "visioncube.operators_cuda" if device == 'cuda' else "visioncube.operators"
    module = getattr(import_module(impl), operator_name)

    # 2个参数
    param1 = get_param(0.0, 1)
    param2 = get_param(0.0, 15)
    for idx in range(len(param1)):
        value1 = param1[idx]
        value2 = param2[idx]
        image = module(value1, value2)(deepcopy(doc))['image']

        image = rgb_to_bgr(image)
        cv2.imwrite(f'output/{round(value1, 2)}-{round(value2, 2)}-.jpg', image)

    # 1个参数
    # param = get_param(0.0, 1)
    # for value in param:
    #     image = module(value)(deepcopy(doc))['image']
    #     image = rgb_to_bgr(image)
    #     cv2.imwrite(f'output/{round(value, 2)}.jpg', image)


if __name__ == '__main__':
    shutil.rmtree('./output', ignore_errors=True)
    os.makedirs('./output')
    pipeline_test()
