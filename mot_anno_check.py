import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np

root_dir = '/home/fatih/disk1/trackeveryseason/images/'

splits = ['test', 'train']

for split in splits:
    data_path = os.path.join(root_dir, split)
    seq_names = [s for s in sorted(os.listdir(data_path))]
    for seq in seq_names:
        anno_path = os.path.join(root_dir, split, seq, 'gt') + '/gt.txt'
        img_path = os.path.join(root_dir, split, seq, 'img1') + '/000001.jpg'
        img = cv2.imread(img_path)
        height, width, c = img.shape
        with open(anno_path, 'r') as fp:
            Lines = fp.readlines()
        new_Lines = []
        for line in Lines:
            anno_str = line.split(',')
            x1 = int(float(anno_str[2]))
            y1 = int(float(anno_str[3]))
            w = int(float(anno_str[4]))
            h = int(float(anno_str[5]))

            x2 = x1 + w
            y2 = y1 + h

            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > width:
                x2 = width
            if y2 > height:
                y2 = height

            w = x2 - x1
            h = y2 - y1

            anno_str[2] = str(x1)
            anno_str[3] = str(y1)
            anno_str[4] = str(w)
            anno_str[5] = str(h)
            new_line = ','.join(anno_str)
            new_Lines.append(new_line)
        with open(anno_path, 'w') as fp:
            fp.writelines(new_Lines)

