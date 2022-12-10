import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt

sompt22 = '/mnt/disk2/golden_phd/mydataset/sompt22'
mot17 = '/mnt/disk2/golden_phd/datasets/fairmot_dataset/MOT17/images'
mot20 = '/mnt/disk2/golden_phd/datasets/fairmot_dataset/MOT20/images'  # train test
out_patch = '/mnt/disk2/golden_phd/experiments/dataset/crop/mot17'
# split = ['test', 'train']
split = 'train'

root = [mot17]

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = int(line_fields[0])
    return amount

for ro in root:
    seqs = os.listdir(os.path.join(ro, split))
    for seq in seqs:
        if 'DPM' in seq or 'SDP' in seq:
            continue
        print(seq)
        gt = os.path.join(ro, split, seq, 'gt', 'gt.txt')
        with open(gt) as fp:
            Lines = fp.readlines()
            Lines.sort(key=my_sort)
            frm_pre = 1
            img1 = cv2.imread(os.path.join(ro, split, seq, 'img1', '000001.jpg'))
            if img1 is None:
                continue
            for ix, line in enumerate(Lines):
                liner = line.split(',')
                frm = int(liner[0])
                id = int(liner[1])
                x = int(liner[2])
                y = int(liner[3])
                w = int(liner[4])
                h = int(liner[5])
                #print(frm)
                os.makedirs(os.path.join(out_patch, split, seq, str(id)), exist_ok=True)
                if frm_pre != frm:
                    height, width, channels = img1.shape
                    if x < 0:
                        x = 0
                    if x > width:
                        x = width
                    if y < 0:
                        y = 0
                    if y > height:
                        y = height                   
                    crop_img = img1[y:y + h, x:x + w]
                    cv2.imwrite(os.path.join(out_patch, split, seq, str(id), str(f'{frm_pre:06}') + '.jpg'), crop_img)
                    frm_pre += 1
                    img1 = cv2.imread(os.path.join(ro, split, seq, 'img1', str(f'{frm_pre:06}')) + '.jpg')
                    if img1 is None:
                        frm_pre += 1
                    else:
                        height, width, channels = img1.shape
                        if h < 5 or w < 5 or height < 0 or width < 0:
                            frm_pre += 1
                else:
                    if img1 is None:
                        frm_pre += 1    
                    else:
                        height, width, channels = img1.shape
                        if h < 5 or w < 5 or height < 0 or width < 0:
                            frm_pre += 1
                            continue
                        if x < 0:
                            x = 0
                        if x + w > width:
                            continue
                        if y < 0:
                            y = 0
                        if y + h > height:
                            continue 
                        crop_img = img1[y:y + h, x:x + w]
                        #print(str(width) + "x" + str(height))
                        cv2.imwrite(os.path.join(out_patch, split, seq, str(id), str(f'{frm_pre:06}') + '.jpg'), crop_img)
                # print(frm_pre)