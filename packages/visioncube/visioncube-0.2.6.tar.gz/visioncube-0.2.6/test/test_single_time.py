#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-06-06
"""
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt
from importlib import import_module

from visioncube import TransformPipeline, get_transforms
from visioncube import get_transforms


def read_image(img_path):
    image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    # image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def pipeline_test(img_path=None):
    device = 'cuda'

    img_path = 'D:\\BaiduNetdiskDownload\\数据\\CF中间盘\\区域2_v3\\OK3\\1\\1.bmp'
    # img_path = 'data/anomaly.jpg'
    image = read_image(img_path)
    doc = {'image': image}

    pipeline = TransformPipeline('test/config.yml', training=True, device=device)
    # pipeline = TransformPipeline([
    #     {'name': 'Add', 'tag': 'train', 'kwargs': {'value': 100}}
    # ], training=True, device=device)

    output = pipeline(doc)
    # print(output['ocr'])
    image1 = output['image']
    # cv2.imwrite('1.jpg', cv2.cvtColor(image1, cv2.COLOR_RGB2BGR))

    plt.imshow(image1, cmap='gray')
    plt.show()


def operator_functional_test():
    """单图单算子随机测试"""

    device = 'cpu'
    impl = "visioncube.operators_cuda" if device == 'cuda' else "visioncube.operators"

    img_path = 'data/ocr_test.jpg'
    image = read_image(img_path)
    doc = {'image': image}

    transforms = get_transforms(device)
    for transform in random.sample(transforms, 10):
        transform_name = transform[0]
        print(transform_name)
        module = getattr(import_module(impl), transform_name)
        doc = module()(doc)

    plt.imshow(doc['image'])
    plt.show()


def functional_test():
    """单图函数调用测试"""
    from visioncube.functional import easyocr as ocr

    img_path = 'data/ocr_test.jpg'
    image = read_image(img_path)

    # image = torch.from_numpy(image)
    # image = hwc_to_chw(image).to('cuda:0')

    out = ocr(image)
    print(out)


if __name__ == '__main__':
    raise SystemExit(pipeline_test())
    # raise SystemExit(functional_test())

    # dir_path = 'D:\\BaiduNetdiskDownload\\数据\\纺织布\\0818A1\\NG\\'
    # for img_path in glob(f'{dir_path}/*.jpg'):
    #     # if '0818A1_0e9cc3986138a6360201908181422334OK' not in img_path:
    #     #     continue
    #
    #     pipeline_test(img_path)
