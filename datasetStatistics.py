import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


somot = '/home/fatih/mnt/trackeveryseason'  # train test
mot17 = '/home/fatih/mnt/fairmot_data/data/MOT17/images'  # train
# split = ['test', 'train']

aspectRatio = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

#
root = [somot, mot17]

histAR = np.zeros((2, 500), dtype=int)  # w/h
histAR_x = np.linspace(0, 10, num=500, dtype=float, endpoint=False)
#print(histAR_x)
histHeight = np.zeros((2, 1920), dtype=int)
histH_x = [x for x in range(0, 1920)]
histDensity = np.zeros((2, 120), dtype=int)
histD_x = [x for x in range(0, 120)]

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[0])
    return amount


for ro in root:
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        if (seq.find('DPM') != -1 and ro == mot17) or ro == somot:
            gt = os.path.join(ro, 'train', seq, 'gt', 'gt.txt')
            with open(gt) as fp:
                Lines = fp.readlines()
                Lines.sort(key=my_sort)
                density = 0
                frm_pre = '1'
                for ix, line in enumerate(Lines):
                    line = line.split(',')
                    frm = line[0]
                    w = line[4]
                    h = line[5]
                    if int(h) == 0:
                        print(ar, h, w, gt, ix)
                    ar = int((float(w) / float(h)) * 50)
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


fig = plt.subplots(figsize=(12, 8))
plt.bar(histAR_x[:100], histAR[0, :100], color='g', width=0.03, label='SOMOT')
plt.bar(histAR_x[:100], histAR[1, :100], color='b', width=0.03, label='MOT17')
plt.ylabel('Frequencies', size=18)
plt.xlabel('Aspect Ratio (w/h)', size=18)
plt.title('Pedestrian Aspect Ratio Frequencies', size=20)
plt.legend()
plt.grid()
plt.savefig('histOfAR.jpg')
plt.show()
plt.close()


fig = plt.subplots(figsize=(12, 8))
plt.bar(histH_x[:400], histHeight[0, :400], color='g', width=8, label='SOMOT')
plt.bar(histH_x[:400], histHeight[1, :400], color='b', width=8, label='MOT17')
plt.ylabel('Frequencies', size=18)
plt.xlabel('Object Height (px)', size=18)
plt.title('Pedestrian Size Frequencies', size=20)
plt.legend()
plt.grid()
plt.savefig('histOfH.jpg')
plt.show()
plt.close()


fig = plt.subplots(figsize=(12, 8))
plt.bar(histD_x[:90], histDensity[0, :90], color='g', width=1.3, label='SOMOT')
plt.bar(histD_x[:90], histDensity[1, :90], color='b', width=1.3, label='MOT17')
plt.ylabel('Frequencies', size=18)
plt.xlabel('Object per Frame', size=18)
plt.title('Pedestrian Densities', size=20)
plt.legend()
plt.grid()
plt.savefig('histOfD.jpg')
plt.show()
plt.close()



"""
np.savetxt('histAR.txt', histAR, delimiter=',', fmt='%d')
np.savetxt('histHeight.txt', histHeight, delimiter=',', fmt='%d')
np.savetxt('histDensity.txt', histDensity, delimiter=',', fmt='%d')
"""
