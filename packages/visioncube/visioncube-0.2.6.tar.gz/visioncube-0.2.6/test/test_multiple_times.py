#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-06-06
"""

import pickle

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import sys

sys.path.append("..")
from visioncube.pipeline import TransformPipeline


def main():
    device = 'cuda'

    filename = '../data/dog-cat.pkl'
    doc = pickle.load(open(filename, 'rb'))

    pipeline = TransformPipeline('../config.yml', training=True, device=device)

    plt.subplot(4, 3, 2)
    plt.imshow(doc['image'])
    bboxes = doc['bboxes']
    for i in range(len(bboxes)):
        bbox = bboxes[i]
        plt.gca().add_patch(
            mpatches.Rectangle((bbox[0], bbox[1]),
                               bbox[2] - bbox[0], bbox[3] - bbox[1],
                               fill=False, edgecolor='red', linewidth=1),
        )

    for i in range(4, 7, 1):
        print(i)

        doc = pickle.load(open(filename, 'rb'))
        output_doc = pipeline(doc)

        plt.subplot(4, 3, i)
        image1 = output_doc['image']

        plt.imshow(image1)

        plt.subplot(4, 3, i + 3)
        heatmap1 = output_doc['heatmap'].copy()
        keypoints = np.array(output_doc['keypoints']).astype(np.int32)
        for kp in keypoints:
            cv2.circle(heatmap1, kp, thickness=-1, radius=int(image1.shape[0] * 0.04),
                       color=[255, 0, 0])
        plt.imshow(heatmap1)

        plt.subplot(4, 3, i + 6)
        mask1 = output_doc['mask']
        plt.imshow(mask1, cmap='gray')

        bboxes1 = output_doc['bboxes']
        for idx in range(len(bboxes1)):
            bbox = output_doc['bboxes'][idx]
            plt.gca().add_patch(
                mpatches.Rectangle((bbox[0], bbox[1]),
                                   bbox[2] - bbox[0], bbox[3] - bbox[1],
                                   fill=False, edgecolor='yellow', linewidth=1.2))
        # break
    plt.show()


if __name__ == '__main__':
    raise SystemExit(main())
    # operators_cuda 56 operators 57
    # print(len(get_transforms('operators')))

# uint8 float64 uint8 uint8 float64 #
# uint8 float32 int32 uint8 float32 # operators_cuda
# uint8 float32 int32 uint8 float32 # operators
