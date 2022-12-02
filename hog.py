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
    # print(orientations)
    x = 0
    feature_vector = np.array([])#shape should be (3780,) by the end of loop (105 blocks * 36 features per block)
    for i in range(0,120,8):
        for j in range(0,56,8):
            x += 1
            print(x)
            block_hist = get_hist(i,j,magnitudes,orientations)
            feature_vector = np.concatenate((feature_vector,block_hist)) 
    print(feature_vector)
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

my_descriptor = get_hog_features("/Users/macuser/Desktop/2022-2023/Semester 3/CSCI1430/finalprojectCSCI1430/hog_car.jpg")
print(np.shape(my_descriptor))

# img = imread("/Users/macuser/Desktop/2022-2023/Semester 3/CSCI1430/finalprojectCSCI1430/hog_car.jpg")
# img = rgb2gray(img)
# img = resize(img,(64,128))
# descriptor, image = hog(img,orientations=9,cells_per_block=(2,2),visualize=True)
# print(descriptor)

# cosine = np.dot(my_descriptor,descriptor)/(np.linalg.norm(my_descriptor)*np.linalg.norm(descriptor))
# print(cosine)




