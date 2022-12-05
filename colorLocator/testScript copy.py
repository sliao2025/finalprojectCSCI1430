import numpy as np
from PIL import Image
from numpy import asarray
from matplotlib import pyplot as plt
import math
from skimage import io, color
import colour
import scipy.signal
import os
import matplotlib.image

error = 80000



callabration1Image = io.imread("cal1.jpg")
callabration1Image = color.rgb2lab(callabration1Image)
callabration1Image = asarray(callabration1Image)
callabration2Image = io.imread("cal2.jpg")
callabration2Image = color.rgb2lab(callabration2Image)
callabration2Image = asarray(callabration2Image)

#background = io.imread("background.jpg")
#background = color.rgb2lab(background)
#background = asarray(background)

def calcDeltaE(img1, img2):
    return np.sqrt(np.sum((img1 - img2) ** 2, axis=-1))/255
'''
def blankBackground(c1, c2, c3):
    colorImage1 = np.full((background.shape), c1)
    colorImage2 = np.full((background.shape), c2)
    colorImage3 = np.full((background.shape), c3)
    delt1 = calcDeltaE(background, colorImage1)
    delt2 = calcDeltaE(background, colorImage2)
    delt3 = calcDeltaE(background, colorImage3)
    m1 = np.mean(delt1)
    m2 = np.mean(delt2)
    m3 = np.mean(delt3)
    newImage = np.zeros((background.shape[0], background.shape[1]))
    for i in range(len(background)):
        for j in range(len(background[0])):
            if(delt1[i][j] < m1/1.5 or delt2[i][j] < m2/1.5 or delt3[i][j] < m3/1.5):
                newImage[i][j] = 1
    newImage = scipy.signal.convolve2d(newImage, np.full((5, 5), 1))
    newImage[newImage >= 1] = 1
    return newImage
'''
def getColor(x, y, image):
    x = round(x)
    y = round(y)
    r = 5
    ret = np.zeros(3)
    for i in range(r):
        for j in range(r):
            ret = ret + image[y-round((r-1)/2)+j][x-round((r-1)/2)+i]
    ret = ret/(r*r)
    return ret

purple = getColor(1426,658,callabration2Image)
red = getColor(1341,333, callabration1Image)
orange = getColor(1379, 561, callabration1Image)

#BlBa = blankBackground(orange, green, purple)



def getAllColor(c1, image):
    colorImage = np.full((testImage.shape), c1)
    delt = calcDeltaE(image, colorImage)
    m = np.mean(delt)
    newImage = np.zeros((testImage.shape[0], testImage.shape[1]))
    newImage[delt < m/1.8] = 1
    return newImage
for i in range(10):
    j = i+1
    name = "left ("+ str(j) +")"
    photoTested = name +".jpg"

    testImage = io.imread(photoTested)
    testImage = color.rgb2lab(testImage)
    testImage = asarray(testImage)

    

    redImage =  getAllColor(red, testImage)
    orangeImage = getAllColor(orange, testImage)
    purpleImage = getAllColor(purple, testImage)

    newImage = np.zeros((redImage.shape[0], redImage.shape[1], 3))
    newImage[:, :, 2] = redImage
    newImage[:, :, 0] = orangeImage
    newImage[:, :, 1] = purpleImage

    temp = np.zeros(newImage.shape)
    temp[:, :, 0] = redImage
    temp[:, :, 1] = redImage
    temp[:, :, 2] = redImage
    redImage = temp

    temp = np.zeros(newImage.shape)
    temp[:, :, 0] = orangeImage
    temp[:, :, 1] = orangeImage
    temp[:, :, 2] = orangeImage
    orangeImage = temp
    
    temp = np.zeros(newImage.shape)
    temp[:, :, 0] = purpleImage
    temp[:, :, 1] = purpleImage
    temp[:, :, 2] = purpleImage
    purpleImage = temp

    #newImage = newImage*255
    print(newImage.shape)
    if(not os.path.exists("results/")):
        os.mkdir("results/")
    if(not os.path.exists("results/" + name + "/")):
        os.mkdir("results/" + name + "/")

    #im = Image.fromarray(blueImage)
    #im.save("results/down ("+ str(j) +")/blue.jpeg")

    #im = Image.fromarray(orangeImage)
    #im.save("results/down ("+ str(j) +")/orange.jpeg")

    #im = Image.fromarray(purpleImage)
    #im.save("results/down ("+ str(j) +")/purple.jpeg")
    matplotlib.image.imsave("results/"+ name +"/all.jpeg", newImage)
    matplotlib.image.imsave("results/"+ name +"/red.jpeg", redImage)
    matplotlib.image.imsave("results/"+ name +"/orange.jpeg", orangeImage)
    matplotlib.image.imsave("results/"+ name +"/purple.jpeg", purpleImage)
