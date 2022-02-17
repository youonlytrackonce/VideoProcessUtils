import sys
sys.path.insert(0, './yolov5')

import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import cv2
from os import listdir


palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


def draw_boxes(img, bbox, identities=None, offset=(0, 0)):
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        color = compute_color_for_labels(id)
        label = '{}{:d}'.format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        cv2.rectangle(
            img, (x1, y1), (x1 + t_size[0] + 3, y1 + t_size[1] + 4), color, -1)
        cv2.putText(img, label, (x1, y1 +
                                 t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
    return img

trackerRoot = '/home/fatih/workspace/Yolov5_DeepSort_Pytorch/'
videoRoot = '/home/fatih/mnt/datasets/MyDataset/AllSeasons/GoldenAnnotationsV4/'
dirs = listdir(videoRoot)
for cam in dirs:
    videos = listdir(videoRoot+cam)
    for video in videos:
        if video.split('.')[-1] == "mp4":
            vidName = video.split('.')[0]
            os.chdir(trackerRoot)
            os.system('python3 {}track.py --source {} --yolo_weights {}/yolov5/weights/crowdhuman_yolov5m.pt '
                      '--classes 0 --save-txt --save-vid --output {}'.format(trackerRoot, videoRoot+cam+'/'+video,
                                                                             trackerRoot, videoRoot+cam+'/'+vidName))
