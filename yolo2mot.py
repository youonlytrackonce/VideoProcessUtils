import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[0])
    return amount

root_img = '/home/ubuntu/phd/sompt22blur/'
root_txt = '/home/ubuntu/phd/sompt22/yolov5det/'

split = ['test', 'train']

for sp in split:
    seqs = os.listdir(os.path.join(root_txt, sp))
    for seq in seqs:
        det = os.listdir(os.path.join(root_txt, sp, seq))
        img = cv2.imread(os.path.join(root_img, sp, seq, 'img1', '000001.jpg'))
        width, height = img.shape[1], img.shape[0]
        with open(os.path.join(root_img, sp, seq, seq + '.txt'), 'a') as gp:
            for tx in det:
                frm = int(tx.split('.')[0])
                with open(os.path.join(root_txt, sp, seq, tx)) as fp:
                    Lines = fp.readlines()
                    for line in Lines:
                        pars = line.split(' ')
                        classN = pars[0]
                        c1 = float(pars[1])*width
                        c2 = float(pars[2])*height
                        imwidth = float(pars[3])*width
                        imheight = float(pars[4])*height
                        x1 = int(c1 - imwidth/2)
                        y1 = int(c2 - imheight/2)
                        x2 = int(c1 + imwidth/2)
                        y2 = int(c2 + imheight/2)
                        gp.write('{}, -1, {}, {}, {}, {}, 1, -1, -1, -1\n'.format(frm, x1, y1, imwidth, imheight))
