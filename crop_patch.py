import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt

sompt22 = '/mnt/disk1/SOMOT22/images'
mot17 = '/mnt/disk2/dataset/dataset_MIX_MOT15_MOT20/MOT17'
mot20 = '/mnt/disk2/dataset/dataset_MIX_MOT15_MOT20/MOT20/images'  # train test
mot20_patch = '/mnt/disk2/dataset/mot_patch/mot20'
# split = ['test', 'train']

root = [mot20]

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = int(line_fields[0])
    return amount

for ro in root:
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        # print(seq)
        gt = os.path.join(ro, 'train', seq, 'gt', 'gt.txt')
        with open(gt) as fp:
            Lines = fp.readlines()
            Lines.sort(key=my_sort)
            frm_pre = 1
            img1 = cv2.imread(os.path.join(ro, 'train', seq, 'img1', '000001.jpg'))
            for ix, line in enumerate(Lines):
                liner = line.split(',')
                frm = int(liner[0])
                id = int(liner[1])
                x = int(liner[2])
                y = int(liner[3])
                w = int(liner[4])
                h = int(liner[5])
                #print(frm)
                os.makedirs(os.path.join(mot20_patch, 'train', seq, str(id)), exist_ok=True)
                if frm_pre != frm:
                    crop_img = img1[y:y + h, x:x + w]
                    cv2.imwrite(os.path.join(mot20_patch, 'train', seq, str(id), str(f'{frm_pre:06}') + '.jpg'), crop_img)
                    frm_pre += 1
                    img1 = cv2.imread(os.path.join(ro, 'train', seq, 'img1', str(f'{frm_pre:06}')) + '.jpg')
                else:
                    crop_img = img1[y:y + h, x:x + w]
                    cv2.imwrite(os.path.join(mot20_patch, 'train', seq, str(id), str(f'{frm_pre:06}') + '.jpg'), crop_img)
                # print(frm_pre)