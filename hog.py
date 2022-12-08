import numpy as np
import cv2
from cv2 import Sobel
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog
import matplotlib.pyplot as plt


def get_hog_features(image):
    img = imread(image)
    img = rgb2gray(img)
    img = resize(img,(64,128))
    x_grad = Sobel(src=img,ddepth=cv2.CV_64F,dx=1,dy=0,ksize=3)
    y_grad = Sobel(src=img,ddepth=cv2.CV_64F,dx=0,dy=1,ksize=3)
    magnitudes = np.sqrt(np.power(y_grad,2) + np.power(x_grad,2))
    orientations = np.arctan2(y_grad,x_grad) * 180/np.pi
    orientations[orientations < 0] += 180
    x = 0
    feature_vector = np.array([])#shape should be (3780,) by the end of loop (105 blocks * 36 features per block)
    for i in range(0,120,8):
        for j in range(0,56,8):
            x += 1
            block_hist = get_hist(i,j,magnitudes,orientations)
            feature_vector = np.concatenate((feature_vector,block_hist)) 
    
    return feature_vector


def get_hist(i,j,magnitudes,orientations):
    #should happen 4 times, sum four 1x9 into 1x36
    block_hist = np.array([]) #should be 1x36 in the end
    for y in range(i,i+16,8):
        # print(i)
        for x in range(j,j+16,8):
            mag = magnitudes[y:y+8,x:x+8]
            ori = orientations[y:y+8,x:x+8]
            hist,_ = np.histogram(ori,bins=9,range=(0,180),weights=mag) #9x1
            block_hist = np.concatenate((block_hist,hist)) #appends 1x9 each time
    #normalize 36x1 by dividing each value by square root of sum of squares
    normalized_hist = block_hist/np.sqrt(np.sum(np.power(block_hist,2)) + 0.00001)
    # normalized_hist = block_hist/np.sqrt(np.linalg.norm(block_hist) + 0.00001)
    return normalized_hist

nums = ["1","2","3","4","5","6","7"]
org = []
red = []
prp = []
o_r = []
o_p = []
r_p = []
for i in range(0,7):
    x = nums[i]
    org1 = get_hog_features("/Users/vasudev/Desktop/CSCI1430/finalprojectCSCI1430/colorLocator/results/left ("+x+")/orange.jpeg")
    red1 = get_hog_features("/Users/vasudev/Desktop/CSCI1430/finalprojectCSCI1430/colorLocator/results/left ("+x+")/red.jpeg")
    prp1 = get_hog_features("/Users/vasudev/Desktop/CSCI1430/finalprojectCSCI1430/colorLocator/results/left ("+x+")/purple.jpeg")
    for j in range(i,7):
        y = nums[j]
        org2 = get_hog_features("/Users/vasudev/Desktop/CSCI1430/finalprojectCSCI1430/colorLocator/results/left ("+y+")/orange.jpeg")
        red2 = get_hog_features("/Users/vasudev/Desktop/CSCI1430/finalprojectCSCI1430/colorLocator/results/left ("+y+")/red.jpeg")
        prp2 = get_hog_features("/Users/vasudev/Desktop/CSCI1430/finalprojectCSCI1430/colorLocator/results/left ("+y+")/purple.jpeg")

        c_org = np.dot(org1,org2)/(np.linalg.norm(org1)*np.linalg.norm(org2))
        c_red = np.dot(red1,red2)/(np.linalg.norm(red1)*np.linalg.norm(red2))
        c_prp = np.dot(prp1,prp2)/(np.linalg.norm(prp1)*np.linalg.norm(prp2))
        c_o_r = np.dot(org1,red2)/(np.linalg.norm(org1)*np.linalg.norm(red2))
        c_o_p = np.dot(org1,prp2)/(np.linalg.norm(org1)*np.linalg.norm(prp2))
        c_r_p = np.dot(red1,prp2)/(np.linalg.norm(red1)*np.linalg.norm(prp2))

        org.append(c_org)
        red.append(c_red)
        prp.append(c_prp)
        o_r.append(c_o_r)
        o_p.append(c_o_p)
        r_p.append(c_r_p)

avg_org = sum(org)/len(org)
avg_red = sum(red)/len(red)
avg_prp = sum(prp)/len(prp)
avg_or = sum(o_r)/len(o_r)
avg_op = sum(o_p)/len(o_p)
avg_rp = sum(r_p)/len(r_p)


print("orange to orange avg =")
print(avg_org)
print("red to red avg =")
print(avg_red)
print("purple to purple avg =")
print(avg_prp)
print("orange to red avg =")
print(avg_or)
print("orange to purple avg =")
print(avg_op)
print("red to purple avg =")
print(avg_rp)










