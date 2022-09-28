import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


somot = '/home/ubuntu/phd/trackeveryseason/images'  # train test
# split = ['test', 'train']

root = [somot]

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[0])
    return amount

for ro in root:
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        gt = os.path.join(ro, 'train', seq, 'gt', 'gt.txt')
        with open(gt) as fp:
            Lines = fp.readlines()
            Lines.sort(key=my_sort)
            frm_pre = 1
            img1 = cv2.imread(os.path.join(ro, 'train', seq, 'img1', '000001.jpg'))
            for ix, line in enumerate(Lines):
                line = line.split(',')
                frm = int(line[0])
                x = int(line[2])
                y = int(line[3])
                w = int(line[4])
                h = int(line[5])
                img1[y:y+int(h/3), x:x+w] = cv2.medianBlur(img1[y:y+int(h/3), x:x+w], 3)
                if frm_pre != frm:
                    cv2.imshow('Face Blur',img1)
                    cv2.waitKey(0) 
                    frm_pre += 1
                    img1 = cv2.imread(os.path.join(ro, 'train', seq, 'img1', str(f'{frm_pre:06}')) + '.jpg')    
                    x = int(line[2])
                    y = int(line[3])
                    w = int(line[4])
                    h = int(line[5])
                    img1[y:y+int(h/3), x:x+w] = cv2.medianBlur(img1[y:y+int(h/3), x:x+w], 3) 

