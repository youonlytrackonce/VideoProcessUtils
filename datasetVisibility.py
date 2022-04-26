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
mot20 = '/mnt/disk1/FairMOT_datasets/MOT20/images'
# split = ['test', 'train']

root = [somot, mot17, mot20]

histOcc = np.zeros((3, 100), dtype=int)  # occ
histOcc_x = [i for i in range(0, 100)]


def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[0])
    return amount


def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    if interArea == 0:
        return 0, 0, 0
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou, boxAArea, interArea

occ = 0

for ro in root:
    seqs = os.listdir(os.path.join(ro, 'train'))
    for seq in seqs:
        if (seq.find('DPM') != -1 and ro == mot17) or ro == somot or ro == mot20:
            gt = os.path.join(ro, 'train', seq, 'gt', 'gt.txt')
            with open(gt) as fp:
                Lines = fp.readlines()
                try:
                    Lines.sort(key=my_sort)
                except:
                    print(ro, seq)
                frm_pre = '1'
                lineSetA = []
                lineSetB = []
                for ix, line in enumerate(Lines):
                    lineSp = line.split(',')
                    frm = lineSp[0]
                    if frm == frm_pre:
                        lineSetA.append(line)
                        lineSetB.append(line)
                    else:
                        for ixA, lineA in enumerate(lineSetA):
                            lineA = lineA.split(',')
                            x1A = float(lineA[2])
                            y1A = float(lineA[3])
                            wA = float(lineA[4])
                            hA = float(lineA[5])
                            x2A = x1A + wA
                            y2A = y1A + hA
                            bboxA = [x1A, y1A, x2A, y2A]
                            for ixB, lineB in enumerate(lineSetB):
                                if ixA == ixB:
                                    continue
                                else:
                                    lineB = lineB.split(',')
                                    x1B = float(lineB[2])
                                    y1B = float(lineB[3])
                                    wB = float(lineB[4])
                                    hB = float(lineB[5])
                                    x2B = x1B + wB
                                    y2B = y1B + hB
                                    bboxB = [x1B, y1B, x2B, y2B]

                                    iou, aArea, interArea = bb_intersection_over_union(bboxA, bboxB)

                                    if iou == 0:
                                        continue
                                    else:
                                        if (y1B < y2A) and (y1B > y1A):
                                            occ += 1
                                            occlusionA = int((interArea/aArea)*100)
                                            if ro == somot:
                                                histOcc[0, occlusionA] += 1
                                            elif ro == mot17:
                                                histOcc[1, occlusionA] += 1
                                            else:
                                                histOcc[2, occlusionA] += 1

                        lineSetA = [line]
                        lineSetB = [line]
                        frm_pre = frm

        else:
            continue

fig = plt.subplots(figsize=(12, 8))
plt.bar(histOcc_x[:], histOcc[2, :], color='r', width=1, label='MOT20', alpha=0.4)
plt.bar(histOcc_x[:], histOcc[0, :], color='g', width=1, label='SOMOT', alpha=0.8)
plt.bar(histOcc_x[:], histOcc[1, :], color='b', width=1, label='MOT17', alpha=0.6)


plt.ylabel('Frequencies', size=18)
plt.xlabel('Occlusion Percent (%)', size=18)
plt.title('Pedestrian Occlusion Frequencies', size=20)
plt.legend()
plt.grid()
plt.savefig('histOfOcc_.jpg')
plt.show()
plt.close()
