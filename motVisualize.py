import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np

video = '/mnt/disk2/dataset/trackeveryseason/cam1/raw_video/cam1_2021-07-06,13_00_05.mp4'
outdir = '/mnt/disk2/dataset/trackeveryseason/cam1/traj_visualize/'
annoTxt = open('/mnt/disk2/dataset/trackeveryseason/cam1/annotations/mot_cvat/gt/gt.txt', 'r')

lines = annoTxt.readlines()
totalLine = len(lines)
colors = [tuple(map(int, color)) for color in np.random.randint(120, 250, (1000, 3))]

cap = cv2.VideoCapture(video)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
bbox = 0

history = 50
cp_list = [(0, 0)] * history
trac_dict = {'1': {'centers': cp_list, 'age': 1}}
"""
print(trac_dict["1"]["age"])
print(trac_dict["1"]["centers"])
print(trac_dict["1"]["centers"][8])
"""

for i in range(1, total_frames + 1):
    ret, frame = cap.read()
    if not ret:
        break
    while int(lines[bbox].split(',')[0]) == i:
        id_ = int(lines[bbox].split(',')[1])
        x1 = float(lines[bbox].split(',')[2])
        y1 = float(lines[bbox].split(',')[3])
        x2 = float(lines[bbox].split(',')[4])
        y2 = float(lines[bbox].split(',')[5])
        if int(x1) < 0:
            x1 = '0'
        if int(x1) < 0:
            x1 = '0'

        cx = x1 + x2 / 2
        cy = y1 + y2 / 2
        x2 += x1
        y2 += y1
        color = colors[id_]
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        if '{}'.format(id_) in trac_dict:
            curr_age = trac_dict['{}'.format(id_)]['age']
            trac_dict['{}'.format(id_)]['age'] += 1
            trac_dict['{}'.format(id_)]['centers'][(curr_age-1) % history] = (cx, cy)
            if curr_age < history:
                for ii in range(curr_age):
                    cen_ = trac_dict['{}'.format(id_)]['centers'][ii]
                    cv2.circle(frame, (int(cen_[0]), int(cen_[1])), 5, color, -1)
                    print("62 id: {}, index: {}".format(id_, ii))
                print(trac_dict['{}'.format(id_)]['centers'])
            else:
                for ii in range(-(curr_age % history), history-(curr_age % history)):
                    cen_ = trac_dict['{}'.format(id_)]['centers'][ii]
                    cv2.circle(frame, (int(cen_[0]), int(cen_[1])), 5, color, -1)
                    print("67 id: {}, index: {}".format(id_, ii))
                print(trac_dict['{}'.format(id_)]['centers'])
        else:
            first_cp = [(0, 0)] * history
            first_cp[0] = (cx, cy)
            first_dic = {'centers': first_cp, 'age': 1}
            trac_dict['{}'.format(id_)] = first_dic
            cv2.circle(frame, (int(cx), int(cy)), 5, color, -1)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, str(id_), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        bbox += 1
        if bbox == totalLine:
            break
    # cv2.imwrite(outdir+'img{}.jpg'.format(i), frame)
    print("frame number: {}".format(i))
    cv2.imshow('Amanda', frame)
    cv2.waitKey(1)
