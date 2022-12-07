import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import io, color
from skimage.transform import resize, rescale


# tryString = "Hello there I am %d" %(4)

coefficient = 6
constant = 0.005

scaling_factor = 8

prev_ratio = 0



for i in range(4):
    path = "./skinAlgorithm/images/image_%d.png" %(i)
    image = io.imread(path)
    image_size = image.shape
    image_size = (image_size[0]//scaling_factor, image_size[1]//scaling_factor, image_size[2])
    image = resize(image, image_size, anti_aliasing= True)
    image = color.rgb2gray(image)

    norm = cv2.normalize(image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    avg_intensity = np.mean(norm)

    for j in range(image_size[0]):
        for k in range(image_size[1]):
            intensity_ratio = norm[j,k]/avg_intensity
            intensity_ratio = intensity_ratio * coefficient
            




