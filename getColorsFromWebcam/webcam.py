import cv2
import numpy as np
from PIL import Image
from numpy import asarray
from matplotlib import pyplot as plt
from skimage import io, color
import os
import matplotlib.image
 
# Opens the inbuilt camera of laptop to capture video.
cap = cv2.VideoCapture(0)
i = 0

callabration1Image = io.imread("cal1.jpg")
callabration1Image = color.rgb2lab(callabration1Image)
callabration1Image = asarray(callabration1Image)
callabration2Image = io.imread("cal2.jpg")
callabration2Image = color.rgb2lab(callabration2Image)
callabration2Image = asarray(callabration2Image)

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

def calcDeltaE(img1, img2):
    return np.sqrt(np.sum((img1 - img2) ** 2, axis=-1))/255

def getAllColor(c1, image):
    colorImage = np.full((image.shape), c1)
    delt = calcDeltaE(image, colorImage)
    m = np.mean(delt)
    newImage = np.zeros((image.shape[0], image.shape[1]))
    newImage[delt < m/1.8] = 1
    return newImage

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
     
    # This condition prevents from infinite looping
    # incase video ends.
    if ret == False:
        break
     
    # Save Frame by Frame into disk using imwrite method
    #cv2.imwrite('extracted_images/Frame'+str(i)+'.jpg', frame)
    i += 1
    name = str(i)
    #matplotlib.image.imsave("results/"+ name +"/default.jpeg", frame)
    frame = color.rgb2lab(frame)


    redImage =  getAllColor(red, frame)
    orangeImage = getAllColor(orange, frame)
    purpleImage = getAllColor(purple, frame)

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

    matplotlib.image.imsave("results/"+ name +"/all.jpeg", newImage)
    matplotlib.image.imsave("results/"+ name +"/red.jpeg", redImage)
    matplotlib.image.imsave("results/"+ name +"/orange.jpeg", orangeImage)
    matplotlib.image.imsave("results/"+ name +"/purple.jpeg", purpleImage)
 
cap.release()
cv2.destroyAllWindows()