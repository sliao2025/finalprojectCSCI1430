from skimage.feature import hog
from skimage import io, color
from skimage.transform import resize, rescale
from skinTest import isolateSkin
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import cv2
import os
import pickle
import numpy as np


# image = color.rgb2gray(image)

# image_size = image.shape

# scaling_factor = 5

# image_size = (image_size[0]//scaling_factor, image_size[1]//scaling_factor)


gestures = ["click", "left", "right", "up"]


X = []
Y = []

for gesture in gestures:
    file_path = "./skinAlgorithm/trainingImages/{}".format(gesture)
    for filename in os.listdir(file_path):
        img = cv2.imread(os.path.join(file_path,filename))[...,::-1]
        if img is not None:
            isolate_image = isolateSkin(img)
            isolate_image = resize(isolate_image, (400,400), anti_aliasing= True)
            fd = hog(isolate_image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(3, 3), feature_vector= True, multichannel= True)
            X.append(fd)
            Y.append(gesture)


clf = svm.LinearSVC()
clf.fit(X,Y)

with open('model.pkl', 'wb') as f:
    pickle.dump(clf,f)

            
