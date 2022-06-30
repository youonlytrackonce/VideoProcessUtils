import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


somot = '/mnt/disk1/trackeveryseason'  # train test
mot17 = '/mnt/disk1/FairMOT_datasets/MOT17/images'  # train
mot20 = '/mnt/disk1/FairMOT_datasets/MOT20/images'  # train

# split = ['test', 'train']

aspectRatio = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

#
root = [somot, mot17, mot20]

histAR = np.zeros((3, 101), dtype=int)  # w/h
histAR_x = np.linspace(0, 1, num=101, dtype=float, endpoint=False)
#print(histAR_x)
histHeight = np.zeros((3, 1920), dtype=int)
histH_x = [x for x in range(0, 1920)]
histDensity = np.zeros((3, 500), dtype=int)
histD_x = [x for x in range(0, 500)]

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[0])
    return amount


for ro in root:
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        if (seq.find('DPM') != -1 and ro == mot17) or ro == somot or ro == mot20:
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
                    ar = float(w) / float(h)
                    if ar <= 1.0:
                        ar = int(ar * 100)
                        if ro == somot:
                            histHeight[0, int(h)] += 1
                            histAR[0, ar] += 1
                        elif ro == mot17:
                            histHeight[1, int(h)] += 1
                            histAR[1, ar] += 1
                        else:
                            histHeight[2, int(h)] += 1
                            histAR[2, ar] += 1


                    if frm == frm_pre:
                        density += 1
                    else:
                        frm_pre = frm
                        if ro == somot:
                            histDensity[0, density] += 1
                        elif ro == mot17:
                            histDensity[1, density] += 1
                        else:
                            histDensity[2, density] += 1
                        density = 1
        else:
            continue



fig = plt.subplots(figsize=(10, 6))
plt.bar(histAR_x[:15000], histAR[2, :15000], color='r', width=0.03, label='MOT20', alpha=0.4)
plt.bar(histAR_x[:15000], histAR[0, :15000], color='g', width=0.03, label='SOMOT22', alpha=0.6)
plt.bar(histAR_x[:15000], histAR[1, :15000], color='b', width=0.03, label='MOT17', alpha=0.8)

plt.ylabel('Distribution', size=25)
plt.xlabel('Aspect Ratio (w/h)', size=25)
plt.title('Pedestrian Aspect Ratio Distribution', size=25)
plt.grid()
plt.savefig('histOfAR.jpg')
plt.show()
plt.close()



fig = plt.subplots(figsize=(10, 6))
plt.bar(histH_x[:400], histHeight[2, :400], color='r', width=8, label='MOT20', alpha=0.4)
plt.bar(histH_x[:400], histHeight[0, :400], color='g', width=8, label='SOMPT22', alpha=0.6)
plt.bar(histH_x[:400], histHeight[1, :400], color='b', width=8, label='MOT17', alpha=0.8)

plt.ylabel('Distribution', size=25)
plt.xlabel('Object Height (px)', size=25)
plt.title('Pedestrian Size Distribution', size=25)
plt.legend(fontsize=25)
plt.grid()
plt.savefig('histOfH.jpg')
plt.show()
plt.close()




fig = plt.subplots(figsize=(10, 6))
plt.bar(histD_x[:250], histDensity[2, :250], color='r', width=1.3, label='MOT20', alpha=0.4)
plt.bar(histD_x[:250], histDensity[0, :250], color='g', width=1.3, label='SOMOT22', alpha=0.6)
plt.bar(histD_x[:250], histDensity[1, :250], color='b', width=1.3, label='MOT17', alpha=0.8)

plt.ylabel('Distribution', size=25)
plt.xlabel('Object per Frame', size=25)
plt.title('Pedestrian Density Distribution', size=25)
plt.grid()
plt.savefig('histOfD.jpg')
plt.show()
plt.close()



"""
np.savetxt('histAR.txt', histAR, delimiter=',', fmt='%d')
np.savetxt('histHeight.txt', histHeight, delimiter=',', fmt='%d')
np.savetxt('histDensity.txt', histDensity, delimiter=',', fmt='%d')
"""
