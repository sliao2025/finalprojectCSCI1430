import numpy as np
import matplotlib.pyplot as plt
import PIL
from skimage import io, color
from skimage.transform import resize, rescale
from skimage.feature import hog
from PIL import Image




#image = io.imread("./skinAlgorithm/trainingImages/click/Edrickclick0.jpg")

def isolateSkin(image):
    image_size = image.shape
    scaling_factor = 3
    image_size = (image_size[0]//scaling_factor, image_size[1]//scaling_factor, image_size[2])
    image = resize(image, image_size, anti_aliasing= True)
    image_hsv = color.rgb2hsv(image)
    image_ycbr = color.rgb2ycbcr(image)

    for i in range(image_size[0]):
        for j in range(image_size[1]):

            #thresholds
            red = image[i,j,0]
            green = image[i,j,1]
            blue = image[i,j,2]

            rgb_1 = (red * 255) > 95
            rgb_2 = (green * 255) > 40
            rgb_3 = (blue * 255) > 20
            rgb_4 = (red > green)
            rgb_5 = (red > blue)
            rgb_6 = (abs(red - green) * 255) > 15

            y = image_ycbr[i,j,0]
            cb = image_ycbr[i,j,1]
            cr = image_ycbr[i,j,2]

            ycbcr_1 = cr > 135
            ycbcr_2 = cb > 85
            ycbcr_3 = y > 80
            ycbcr_4 = cr <= ((1.5862 * cb) + 20)
            ycbcr_5 = cr >= ((0.3448*cb) + 76.2069)
            ycbcr_6 = cr >= ((-4.5652 * cb) + 234.5652)
            ycbcr_7 = cr <= ((-1.15 * cb) + 301.75)
            ycbcr_8 = cr <= ((-2.2857 * cb) + 432.85)

            h = image_hsv[i,j,0]
            s = image_hsv[i,j,1]

            hsv_1 = (h >= 0) and (h <= 50)
            hsv_2 = (s >= 0.23) and (s <= 0.68)

            if not ((hsv_1 and hsv_2 and rgb_1 and rgb_2 and rgb_3 and rgb_4 and rgb_5 and rgb_6)
                or (rgb_1 and rgb_2 and rgb_3 and rgb_4 and rgb_5 and rgb_6 and ycbcr_1
                    and ycbcr_2 and ycbcr_3 and ycbcr_4 and ycbcr_5 and ycbcr_6 and ycbcr_7 and ycbcr_8)):

                image[i,j,0] = 0
                image[i,j,1] = 0
                image[i,j,2] = 0
    return image


# fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
#                     cells_per_block=(1, 1), visualize=True)



