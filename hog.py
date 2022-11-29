import numpy as np
from cv2 import Sobel
import matplotlib.pyplot as plt



def get_hog_features(image):
    x_grad = Sobel(src=image,ddepth=-1,dx=1,dy=0,ksize=3)
    y_grad = Sobel(src=image,ddepth=-1,dx=0,dy=1,ksize=3)
    magnitudes = np.sqrt(np.power(y_grad,2) + np.power(x_grad,2))
    orientations = np.arctan2(y_grad,x_grad) 

    #can we use np.histogram???
    #next steps -> bins and histograms

    print(orientations)
    plt.imshow(image)
    plt.show()


    


