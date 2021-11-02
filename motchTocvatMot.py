import pafy
import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np

sourceTxt = open('/home/ubuntu/phd/goldenSample/mot_anno/set1/cam23/cam23_2021-08-10,12_30_45.txt', 'r')
destTxt = open('/home/ubuntu/phd/goldenSample/mot_anno/set1/cam23/cam23_2021-08-10,12_30_45_cvat.txt', 'w')

lines = sourceTxt.readlines()
line_com =[]

for inx, line in enumerate(lines):
    line = line.split(',')
    line_com = line[0:2]
    for i in range(2,6):
        newstr = int(float(line[i]))
        newstr = str(newstr)
        line_com.append(newstr)
    line_com = ','.join(line_com)
    line_com = line_com + ',1,1,1.0\n'
    destTxt.write(line_com)



"""
for inx, line in enumerate(lines):
    line = line.split(',')
    line_com = line[0:6]
    line_com = ','.join(line_com)
    line_com = line_com + ',1,1,1.0\n'
    destTxt.write(line_com)
"""


