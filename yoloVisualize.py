import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np


root_img = '/mnt/disk1/trackeveryseason/images/train/cam2_2021-02-23,04_00_40/img1/'
root_txt = '/mnt/disk1/trackeveryseason/annotations/train/cam2_2021-02-23,04_00_40/img1/'
frm = '000001'
img = cv2.imread(root_img + frm +'.jpg')
width, height = img.shape[1], img.shape[0]
colors = [tuple(map(int, color)) for color in np.random.randint(120, 250, (1000, 3))]

with open(root_txt + frm +'.txt') as f:
    lines = f.readlines()

    for line in lines:
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
        color = colors[int(classN)]
        cv2.putText(img,classN, (x1, y1+10), cv2.FONT_HERSHEY_SIMPLEX, 1, 1, 2)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
    cv2.imshow('yolo', img)
    cv2.waitKey(0)
    # closing all open windows
    cv2.destroyAllWindows()
