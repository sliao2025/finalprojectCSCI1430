from ast import Pass
import numpy as np
import cv2
from cv2 import Sobel
import matplotlib.pyplot as plt

def get_hog_features(image):
    x_grad = Sobel(src=image,ddepth=cv2.CV_64F,dx=1,dy=0,ksize=3)
    y_grad = Sobel(src=image,ddepth=cv2.CV_64F,dx=0,dy=1,ksize=3)
    magnitudes = np.sqrt(np.power(y_grad,2) + np.power(x_grad,2))
    orientations = np.arctan2(y_grad,x_grad) 

    cells = np.array((16,8))
    feature_vector = np.array([])
    for i in range(0,128,16):
        for j in range(0,64,16):
            block_hist = get_hist(i,j,magnitudes,orientations)
            feature_vector = np.concatenate((feature_vector,block_hist)) #shape should be (3780,)

    pass   
    #can we use np.histogram???
    #next steps -> bins and histograms

def get_hist(i,j,magnitudes,orientations):
    #should happen 4 times, sum four 9x1 into 36x1
    block_hist = np.array([])
    for y in range(i,i+16,8):
        for x in range(j,j+16,8):
            mag = magnitudes[y:y+8,x:x+8]
            ori = orientations[y:y+8,x:x+8]
            hist,_ = np.histogram(ori,bins=9,range=(0,180),weights=mag) #9x1
            block_hist = np.concatenate((block_hist,hist))
    #normalize 36x1 by dividing each value by square root of sum of squares
    normalized_hist = block_hist/np.sqrt(np.sum(np.power(block_hist,2)))
    


    


