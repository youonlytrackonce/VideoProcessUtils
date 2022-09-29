import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


somot = '/home/ubuntu/phd/sompt22'  # train test
sompt22blur = '/home/ubuntu/phd/sompt22blur'
# split = ['test', 'train']

root = [somot]

def my_sort(linex):
    line_fields = linex.strip().split(',')
    amount = float(line_fields[0])
    return amount

for ro in root:
    seqs = os.listdir(os.path.join(ro, 'test'))
    for seq in seqs:
        if seq != 'SOMPT22-06' :
            gt = os.path.join(ro, 'test', seq, 'gt', 'gt.txt')
            with open(gt) as fp:
                Lines = fp.readlines()
                Lines.sort(key=my_sort)
                frm_pre = 1
                img1 = cv2.imread(os.path.join(ro, 'test', seq, 'img1', '000001.jpg'))
                os.makedirs(os.path.join(sompt22blur, 'test', seq, 'img1'), exist_ok=True)
                for ix, line in enumerate(Lines):
                    liner = line.split(',')
                    frm = int(liner[0])
                    x = int(liner[2])
                    y = int(liner[3])
                    w = int(liner[4])
                    h = int(liner[5])
                    #print(frm)
                    if frm_pre != frm:
                        cv2.imwrite(os.path.join(sompt22blur, 'test', seq, 'img1', str(f'{frm_pre:06}')) + '.jpg', img1)
                        frm_pre += 1
                        img1 = cv2.imread(os.path.join(ro, 'test', seq, 'img1', str(f'{frm_pre:06}')) + '.jpg')
                        img1[y:y+int(h/4), x:x+w] = cv2.GaussianBlur(img1[y:y+int(h/4), x:x+w], (5, 5), 0) #cv2.medianBlur(img1[y:y+int(h/4), x:x+w], 3)
                    else:
                        img1[y:y+int(h/4), x:x+w] = cv2.GaussianBlur(img1[y:y+int(h/4), x:x+w], (5, 5), 0) #cv2.medianBlur(img1[y:y+int(h/4), x:x+w], 3)
                cv2.imwrite(os.path.join(sompt22blur, 'test', seq, 'img1', str(f'{frm:06}')) + '.jpg', img1)

            """
            line = line.split(',')
            frm = int(line[0])
            x = int(line[2])
            y = int(line[3])
            w = int(line[4])
            h = int(line[5])
            img1[y:y+int(h/3), x:x+w] = cv2.medianBlur(img1[y:y+int(h/3), x:x+w], 3)
            #img1[y:y+int(h/3), x:x+w] = cv2.GaussianBlur(img1[y:y+int(h/3), x:x+w], (5,5),0)
            if frm_pre != frm:
                #cv2.imshow('Face Blur',img1)
                #cv2.waitKey(0) 
                #cv2.destroyAllWindows() 
                cv2.imwrite(os.path.join(sompt22blur, 'train', seq, 'img1', str(f'{frm_pre:06}')) + '.jpg', img1)
                frm_pre += 1
                img1 = cv2.imread(os.path.join(ro, 'train', seq, 'img1', str(f'{frm_pre:06}')) + '.jpg')    
                x = int(line[2])
                y = int(line[3])
                w = int(line[4])
                h = int(line[5])
                img1[y:y+int(h/3), x:x+w] = cv2.medianBlur(img1[y:y+int(h/3), x:x+w], 3)
                #img1[y:y+int(h/3), x:x+w] = cv2.GaussianBlur(img1[y:y+int(h/3), x:x+w], (5,5),0)
            """

