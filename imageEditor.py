import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter

import matplotlib.pyplot as plt
import requests
#from cairosvg import svg2png

def rect_with_rounded_corners(image, r, t, c):
    """
    :param image: image as NumPy array
    :param r: radius of rounded corners
    :param t: thickness of border
    :param c: color of border
    :return: new image as NumPy array with rounded corners
    """

    c += (255, )

    h, w = image.shape[:2]

    # Create new image (three-channel hardcoded here...)
    new_image = np.ones((h+2*t, w+2*t, 4), np.uint8) * 255
    new_image[:, :, 3] = 0

    # Draw four rounded corners
    new_image = cv2.ellipse(new_image, (int(r+t/2), int(r+t/2)), (r, r), 180, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(w-r+3*t/2-1), int(r+t/2)), (r, r), 270, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(r+t/2), int(h-r+3*t/2-1)), (r, r), 90, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(w-r+3*t/2-1), int(h-r+3*t/2-1)), (r, r), 0, 0, 90, c, t)

    # Draw four edges
    new_image = cv2.line(new_image, (int(r+t/2), int(t/2)), (int(w-r+3*t/2-1), int(t/2)), c, t)
    new_image = cv2.line(new_image, (int(t/2), int(r+t/2)), (int(t/2), int(h-r+3*t/2)), c, t)
    new_image = cv2.line(new_image, (int(r+t/2), int(h+3*t/2)), (int(w-r+3*t/2-1), int(h+3*t/2)), c, t)
    new_image = cv2.line(new_image, (int(w+3*t/2), int(r+t/2)), (int(w+3*t/2), int(h-r+3*t/2)), c, t)

    # Generate masks for proper blending
    mask = new_image[:, :, 3].copy()
    mask = cv2.floodFill(mask, None, (int(w/2+t), int(h/2+t)), 128)[1]
    mask[mask != 128] = 0
    mask[mask == 128] = 1
    mask = np.stack((mask, mask, mask), axis=2)

    # Blend images
    temp = np.zeros_like(new_image[:, :, :3])
    temp[(t-1):(h+t-1), (t-1):(w+t-1)] = image.copy()
    new_image[:, :, :3] = new_image[:, :, :3] * (1 - mask) + temp * mask

    # Set proper alpha channel in new image
    temp = new_image[:, :, 3].copy()
    new_image[:, :, 3] = cv2.floodFill(temp, None, (int(w/2+t), int(h/2+t)), 255)[1]

    return new_image



images_dir = '/home/fatih/mnt/trackeveryseason/album/'
fig, axes = plt.subplots(nrows=2, ncols=4,figsize=(19.2, 10.8))
seqs = os.listdir(images_dir)
for ix, seq in enumerate(seqs):
    img = os.listdir(images_dir + seq)
    new_img = cv2.imread(images_dir + seq + '/' + img[0])
    # cv2.imshow('{}'.format(seq), new_img)
    new_img = rect_with_rounded_corners(new_img, 100, 20, (255, 255, 255))
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    row = ix / 4
    col = ix % 4
    axes[int(row),col].imshow(new_img)
    axes[int(row),col].axis('off')
"""
plt.subplots_adjust(left=0,
                    bottom=0,
                    right=1,
                    top=1,
                    wspace=0,
                    hspace=0)
"""
fig.tight_layout(h_pad=-100, w_pad = 0)
plt.savefig('album.png', dpi=100)
fig.show()
plt.axis('off')
"""
new_img = cv2.imread('album.png')
crop_img = new_img[480:600, 190:1730]
cv2.imwrite('album_crop.png', crop_img)
"""

