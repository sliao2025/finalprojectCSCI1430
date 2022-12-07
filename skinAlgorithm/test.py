from skimage.feature import hog
from skimage import io, color
from skimage.transform import resize, rescale
from skinTest import isolateSkin
from sklearn import svm
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import cv2
import os
import pickle
import numpy as np


with open('model.pkl', 'rb') as f:
    clf2 = pickle.load(f)


image = io.imread("./skinAlgorithm/trainingImages/right/Edrickright0.jpg")
#image2 = io.imread("./skinAlgorithm/trainingImages/up/Edrickup0.jpg")

image = isolateSkin(image)

image = resize(image, (400,400), anti_aliasing= True)

testers = np.ndarray((2,38088))


fd = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(3, 3), feature_vector= True, multichannel= True)

fc = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(3, 3), feature_vector= True, multichannel= True)



np.append(testers,fd)
np.append(testers,fc)


prediction = clf2.predict(testers)


cr = classification_report(["right", "right"], prediction)

print(cr)



print(prediction)