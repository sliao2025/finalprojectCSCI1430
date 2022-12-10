from sift import SIFT
import cv2
import matplotlib.pyplot as plt

sift = SIFT(reference='finalprojectCSCI1430/both.png',
            arrow_f='finalprojectCSCI1430/stencils/front/arrow_f.jpeg',
            arrow_b='finalprojectCSCI1430/stencils/back/arrow_b.jpeg')

image = 'finalprojectCSCI1430/cross sample up.jpeg'


plt.imshow(cv2.imread('finalprojectCSCI1430/both.png'))
plt.show()
sift.get_SIFT_features(image)
sift.show_SIFT_features()
