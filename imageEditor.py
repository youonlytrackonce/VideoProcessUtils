import cv2
import time
import os
import sys
from datetime import datetime
import shutil
import numpy as np
from operator import itemgetter

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from glob import glob


images_dir = '/home/fatih/phd/VideoProcessUtils/'
def plot_album(album_name):
    fig, axes = plt.subplots(nrows=1, ncols=3)
    # this assumes the images are in images_dir/album_name/<name>.jpg
    image_paths = glob(images_dir + album_name + '/*.jpg')
    for imp, ax in zip(image_paths, axes.ravel()):
        img = mpimg.imread(imp)
        ax.imshow(img)
        ax.axis('off')
    fig.tight_layout()
    plt.savefig('hists.jpg', dpi=300)
    fig.show()


plot_album('hists')