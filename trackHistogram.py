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


root = [somot, mot17, mot20]

histTrack = np.zeros((3, 5000), dtype=int)
histT_x = [x for x in range(0, 5000)]

window = 1500

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[1])
    return amount


for ro in root:
    print(ro)
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        if (seq.find('DPM') != -1 and ro == mot17) or ro == somot or ro == mot20:
            gt = os.path.join(ro, 'train', seq, 'gt', 'gt.txt')
            cnt = 0
            id_init = 1
            with open(gt) as fp:
                Lines = fp.readlines()
                Lines.sort(key=my_sort)
                for ix, line in enumerate(Lines):
                    line = line.split(',')
                    ID = int(line[1])
                    #print('ID: {}'.format(ID))
                    #print('id_init: {}'.format(id_init))
                    if id_init == ID:
                        cnt += 1
                        #print('cnt: {}'.format(cnt))
                    else:
                        if ro == somot:
                            histTrack[0, cnt] += 1
                        elif ro == mot17:
                            histTrack[1, cnt] += 1
                        else:
                            histTrack[2, cnt] += 1
                        cnt = 1
                        id_init = ID
        else:
            continue

fig = plt.subplots(figsize=(10, 6))
MOT20 = sum(histTrack[2, :])
print('MOT20: {}'.format(MOT20))
SOMPT22 = sum(histTrack[0, :])
print('SOMPT22: {}'.format(SOMPT22))
MOT17 = sum(histTrack[1, :])
print('MOT17: {}'.format(MOT17))

for i in range(window):
    if histTrack[2, i] > 12:
        histTrack[2, i] = 12
    if histTrack[1, i] > 12:
        histTrack[1, i] = 12
    if histTrack[0, i] > 12:
        histTrack[0, i] = 12


plt.bar(histT_x[:window], histTrack[2, :window], color='r', width=10, label='MOT20', alpha=0.5)
plt.bar(histT_x[:window], histTrack[1, :window], color='b', width=10, label='MOT17', alpha=0.7)
plt.bar(histT_x[:window], histTrack[0, :window], color='g', width=10, label='SOMPT22', alpha=0.9)

plt.ylabel('Distribution', size=25)
plt.xlabel('Track length', size=25)
plt.title('Pedestrian Track Distribution', size=25)
plt.grid()
plt.savefig('histOfTrack.jpg')
plt.show()
plt.close()




np.savetxt('histTrack.txt', histTrack, delimiter=',', fmt='%d')

