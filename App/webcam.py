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
print(cap)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
i = 0
'''
callabration1Image = io.imread("cal1.jpg")
callabration1Image = color.rgb2lab(callabration1Image)
callabration1Image = asarray(callabration1Image)
callabration2Image = io.imread("cal2.jpg")
callabration2Image = color.rgb2lab(callabration2Image)
callabration2Image = asarray(callabration2Image)
callabration3Image = io.imread("cal3.jpg")
callabration3Image = color.rgb2lab(callabration3Image)
callabration3Image = asarray(callabration3Image)
callabration4Image = io.imread("cal4.jpg")
callabration4Image = color.rgb2lab(callabration4Image)
callabration4Image = asarray(callabration4Image)
callabration5Image = io.imread("cal 5.jpg")
callabration5Image = color.rgb2lab(callabration5Image)
callabration5Image = asarray(callabration5Image)
callabration6Image = io.imread("cal 6.jpg")
callabration6Image = color.rgb2lab(callabration6Image)
callabration6Image = asarray(callabration6Image)

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
orange = getColor(1596, 839, callabration5Image)
brown = getColor(1569, 720, callabration3Image)
yellow = getColor(1560, 592, callabration5Image)
pink = getColor(1407, 517, callabration6Image)
'''
def calcDeltaE(img1, img2):
    return np.sqrt(np.sum((img1 - img2) ** 2, axis=-1))/255

def getAllColor(c1, image):
    colorImage = np.full((image.shape), c1)
    delt = calcDeltaE(image, colorImage)
    m = np.mean(delt)
    newImage = np.zeros((image.shape[0], image.shape[1]))
    print(m/2)
    newImage[delt < 0.16] = 1
    return newImage

yellow = avgColors[1]
orange = avgColors[0]

cap = cv2.VideoCapture(0)
i = 0
sift = SIFT(reference='../reference.png',
            arrow_f='../stencils/front/arrow_f.jpeg',
            arrow_b='../stencils/back/arrow_b.jpeg')
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


    #redImage =  getAllColor(pink, frame)
    orangeImage = getAllColor(orange, frame)
    yellowImage = getAllColor(yellow, frame)

    newImage = np.zeros((orangeImage.shape[0], orangeImage.shape[1], 3))
    #newImage[:, :, 2] = redImage
    newImage[:, :, 0] = orangeImage
    newImage[:, :, 1] = yellowImage

    sift.get_SIFT_features(newImage)
    sift.show_SIFT_features()

 
cap.release()
cv2.destroyAllWindows()  