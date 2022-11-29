import numpy as np
from skimage.io import imread
from skimage.transform import resize
from hog import get_hog_features

def get_features():
    image_paths = [] #fill with image paths
    #images may need to be cropped from initial webcam input to a bounding box
    image_paths.append("/Users/macuser/Desktop/Screen Shot 2022-07-03 at 12.21.49 AM.png")
    print(image_paths)
    for i in image_paths:
        image = imread[i]
        image = resize(image,(64,128))
        hog_feature = get_hog_features(image)

