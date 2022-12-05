import numpy as np
from PIL import Image
from numpy import asarray
from matplotlib import pyplot as plt
import math

error = 10
photoTested = "side3.jpg"
cropStart = [242, 533]
cropEnd = [738, 886]

callabrationImage = Image.open("calabration.jpg")
callabrationImage = asarray(callabrationImage)

background = Image.open("background.jpg")
background = asarray(background)

print(callabrationImage.shape)

def getColor(x, y, image):
    x = round(x)
    y = round(y)
    r = 15
    ret = np.zeros(3)
    for i in range(r):
        for j in range(r):
            ret = ret + image[y-round((r-1)/2)+j][x-round((r-1)/2)+i]
    ret = ret/(r*r)
    return ret

purple = getColor(651,551,callabrationImage)
green = getColor(787,541, callabrationImage)
orange = getColor(696, 739, callabrationImage)

def withinColor(c1, c2, error):
    errorTotal = 0
    for i in range(3):
        errorTotal = errorTotal + abs(c1[i] - c2[i])
    return errorTotal < error
def getError(c1, c2):
    errorTotal = 0
    for i in range(3):
        errorTotal = errorTotal + abs(c1[i] - c2[i])
    return errorTotal

blackOut = np.full((len(background), len(background[0])), False)

for i in range(len(background)):
    for j in range(len(background[0])):
        if withinColor(purple, background[i][j], error*2) or withinColor(orange, background[i][j], error*2) or withinColor(green, background[i][j], error*2):
            for i2 in range(21):
                for j2 in range(21):
                    y = i+i2-10
                    x = j+j2-10
                    if x > 0 and x < len(background[0]) and y > 0 and y < len(background):
                        blackOut[y][x] = True 

testImage = Image.open(photoTested)
testImage = asarray(testImage)

newTest = np.zeros(testImage.shape)
for i in range(len(testImage)):
    print(i)
    for j in range(len(testImage[0])):
        if blackOut[i][j]:
            newTest[i][j] = [1, 0, 0]#
        else:
            newTest[i][j] = [1, 1, 1]
plt.imshow(newTest, interpolation='nearest')
plt.show()


def getAverageLocation(c1, image):
    sum = np.zeros(2)
    total = 0
    for i in range(cropStart[1], cropEnd[1]):
        for j in range(cropStart[0], cropEnd[0]):
            if(withinColor(image[i][j], c1, error) and not blackOut[i][j]):
                curError = getError(image[i][j], c1)
                sum = sum + np.array([i, j])*(error-curError)
                total = total + error - curError
    if total == 0:
        return [-1, -1]
    return sum/total

def getAverageLocationClose(c1, pos, image):
    if pos[0] == -1:
        return [-1, -1]
    sum = np.zeros(2)
    total = 0
    r = 150
    for i in range(r):
        for j in range(r):
            y = i+round(pos[0])-(round(r/2))
            x = j+round(pos[1])-(round(r/2))
            if(x > 0 and x < len(image[0]) and y > 0 and y < len(image)):
                if(withinColor(image[y][x], c1, error) and not blackOut[y][x]):
                    curError = getError(image[y][x], c1)
                    sum = sum + np.array([y, x])*math.exp(-curError)
                    total = total + math.exp(-curError)
    if total == 0:
        return [-1, -1]
    return sum/total

orangeLoc = getAverageLocationClose(orange, getAverageLocation(orange, testImage), testImage)
purpleLoc = getAverageLocationClose(purple, getAverageLocation(purple, testImage), testImage)
greenLoc = getAverageLocationClose(green, getAverageLocation(green, testImage), testImage)
#greenLoc = getAverageLocation(green, testImage)

print(orangeLoc)
print(purpleLoc)
print(greenLoc)

if withinColor(getColor(orangeLoc[1], orangeLoc[0], testImage), orange, error*3) and withinColor(getColor(purpleLoc[1], purpleLoc[0], testImage), purple, error*3) and withinColor(getColor(greenLoc[1], greenLoc[0], testImage), green, error*3):
    print("hand found")
else:
    print("no hand")