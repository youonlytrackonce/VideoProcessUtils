import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


somot = '/home/fatih/phd/yolov5/runs/detect/dets'  # train test
result = '/home/fatih/phd/yolov5/runs/detect/stats.txt'

wr = open(result, 'a')

vidHeight = 1080

seqs = os.listdir(somot)
for seq in seqs:
    if seq == 'cam2 2021-02-23,04 00 40' or seq == 'cam2 2021-02-23,18 00 04':
        vidHeight = 720
    else:
        vidHeight = 1080
    txt_list = os.path.join(somot, seq)
    txts = os.listdir(txt_list)
    wr.write('Seq: ' + seq + ' ')
    wr.write('fr: ' + str(len(txts)) + ' ')
    nDet = 0
    min_height = vidHeight
    max_height = 0
    for txt in txts:
        with open(os.path.join(somot, seq, txt)) as fp:
            Lines = fp.readlines()
            nDet += len(Lines)
            for ix, line in enumerate(Lines):
                line = line.split(' ')
                height = line[4]
                height = float(height)
                height *= vidHeight
                if height < min_height:
                    min_height = height
                if height > max_height:
                    max_height = height
    wr.write('nDet: ' + str(nDet) + ' ')
    wr.write('nDet/fr: ' + str(nDet/len(txts)) + ' ')
    wr.write('min height : ' + str(min_height) + ' ')
    wr.write('max height : ' + str(max_height) + '\n')









