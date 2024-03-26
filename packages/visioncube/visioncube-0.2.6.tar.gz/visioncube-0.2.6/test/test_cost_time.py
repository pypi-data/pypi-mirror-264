#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-06-15
"""
import time
import sys

t0 = time.time()
import os
import cv2 as cv
import numpy as np

sys.path.append("..")
from visioncube import TransformPipeline

os.environ['CUDA_VISIBLE_DEVICES'] = '1' #
t1 = time.time()


def write(doc):
    from uuid import uuid1
    save_dir = f'output/{str(uuid1())}'
    os.makedirs('output/', exist_ok=True)
    image = cv.cvtColor(doc['image'].astype('uint8'), cv.COLOR_RGB2BGR)
    mask = doc['mask']
    mask[mask != 0] = 255
    bboxes = doc['bboxes']

    for bbox in bboxes:
        bbox = np.array(bbox, np.int32)
        cv.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)

    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

    cv.imwrite(f'{save_dir}-image.jpg', image)
    cv.imwrite(f'{save_dir}-mask.jpg', mask)


def main():
    print('============== import package ==============')

    # device = 'operators_cuda'
    device = sys.argv[1]
    img_path = '../data/lena.jpeg'
    image = cv.imread(img_path, cv.IMREAD_COLOR)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    t2 = time.time()

    pipeline = TransformPipeline('../test_image_transforms1.yml', training=True, device=device)

    doc = {
        'image': image,
        # 'bboxes': [
        #     [34.35483870967742, 2.0161290322580645, 425.64516129032256, 447.8225806451613, 1],
        #     [429.51612903225805, 85.24193548387096, 719.0, 476.82198000212, 2]
        # ],
        # 'mask': cv.imread('../data/dog-cat-mask.jpg', 0),
    }
    image1 = pipeline(doc)['image']

    t3 = time.time()
    cost_time = []
    for i in range(1000):
        doc = {'image': image}
        output_doc = pipeline(doc)
        # write(output_doc)
        # print(doc['image'].shape)
        cost_time.append(output_doc['cost_time'])

    print('处理一张图片耗时(ms): ', np.mean(cost_time) * 1000)

    t4 = time.time()
    print('导包: ', t1 - t0)
    print('加载图片: ', t2 - t1)
    print('预热: ', t3 - t2)
    print('预处理: ', t4 - t3)
    print('总耗时: ', t4 - t0)


if __name__ == '__main__':
    raise SystemExit(main())
    # print(get_transforms(device='operators'))
