import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np

somot = '/home/fatih/phd/CenterNet/data/trackeveryseason' # train test
mot17 = '/mnt/disk1/FairMOT_datasets/MOT17/images' #train
#split = ['test', 'train']

aspectRatio = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

root = [somot, mot17]

histAR = np.zeros((2, 500), dtype=int)  # w/h
histHeight = np.zeros((2, 1920), dtype=int)
histDensity = np.zeros((2, 100), dtype=int)

for ro in root:
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        if (seq.find('DPM') != -1 and ro == mot17) or ro == somot:
            gt = os.path.join(ro, 'train', seq, 'gt', 'gt.txt')
            with open(gt) as fp:
                Lines = fp.readlines()
                density = 0
                frm_pre = '1'
                for ix, line in enumerate(Lines):
                    line = line.split(',')
                    frm = line[0]
                    w = line[4]
                    h = line[5]
                    if int(h) == 0:
                        print(ar, h, w, gt, ix)
                    ar = int((int(w)/int(h))*50)
                    if ro == somot:
                        histHeight[0, int(h)] += 1
                        histAR[0, ar] += 1
                    else:
                        histHeight[1, int(h)] += 1
                        histAR[1, ar] += 1

                    if frm == frm_pre:
                        density += 1
                    else:
                        frm_pre = frm
                        if ro == somot:
                            histDensity[0, density] += 1
                        else:
                            histDensity[1, density] += 1
                        density = 1
        else:
            continue

np.savetxt('histAR.txt', histAR, delimiter=',', fmt='%d')
np.savetxt('histHeight.txt', histHeight, delimiter=',', fmt='%d')
np.savetxt('histDensity.txt', histDensity, delimiter=',', fmt='%d')
