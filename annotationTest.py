import pafy
import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np

video = '/home/ubuntu/phd/goldenSample/mot_anno/set2/cam12/cam12_2021-07-29,18_09_01.mp4'
outdir = '/home/ubuntu/phd/goldenSample/mot_anno/set2/cam12/test/'
annoTxt = open('/home/ubuntu/phd/goldenSample/mot_anno/set2/cam12/cam12_2021-07-29,18_09_01_result.txt', 'r')

lines = annoTxt.readlines()
totalLine = len(lines)
colors = [tuple(map(int, color)) for color in np.random.randint(120, 250, (1000, 3))]

cap = cv2.VideoCapture(video)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
bbox = 0
for i in range(1, total_frames+1):
    ret, frame = cap.read()
    if not ret:
        break
    while int(lines[bbox].split(',')[0]) == i:
        id = int(lines[bbox].split(',')[1])
        x1 = float(lines[bbox].split(',')[2])
        y1 = float(lines[bbox].split(',')[3])
        x2 = float(lines[bbox].split(',')[4])
        y2 = float(lines[bbox].split(',')[5])
        if int(x1) < 0:
            x1 = '0'
        if int(x1) < 0:
            x1 = '0'

        x2 += x1
        y2 += y1
        color = colors[id]
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, str(id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        bbox += 1
        if bbox == totalLine:
            break
    cv2.imwrite(outdir+'img{}.jpg'.format(i), frame)





    """
    folders = os.listdir(outDir)
    frmNum = 1800
    for count, line in enumerate(lines):
        commState = line.split(' ')[0]
        if commState != '#':
            camID = line.split(' ')[0]
            camURL = line.split(' ')[1]
            x1, y1, x2, y2 = line.split(' ')[2:6]  # crop coordinates
            resolution = line.split(' ')[6]
            width = int(resolution.split('x')[0])
            height = int(resolution.split('x')[1])
            fps = line.split(' ')[7]
            print('CamID: {}, URL: {}, x1,y1,x2,y2: {},{},{},{}, res: {}, fps: {}'.format(camID, camURL, x1, y1, x2, y2,
                                                                                          resolution, fps))
            vids = os.listdir(outDir)
            print(vids)
            for vid in vids:
                capTime = vid.split('.')[0]
                inputVid = outDir + vid
                outputVid = outDir + 'converted/cam{}_{}.mp4'.format(camID, capTime)
                cmd_str = "ffmpeg -i {} -vf \"crop={}:{}:{}:{},scale={}:{}\" -c:v libx264 -preset slow -crf 18 -an {}".format(inputVid, int(x2)-int(x1), int(y2)-int(y1), int(x1), int(y1), width, height, outputVid)
                os.system(cmd_str)
                # os.remove(inputVid)
                print('cam{} OK! {}'.format(camID, capTime))
    """