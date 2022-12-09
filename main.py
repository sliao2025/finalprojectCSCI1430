from sift import SIFT

sift = SIFT(cross='finalprojectCSCI1430/stencils/front/ cross.jpeg',
            star='finalprojectCSCI1430/stencils/back/star.jpeg',
            arrow_f='finalprojectCSCI1430/stencils/front/arrow_f.jpeg',
            arrow_b='finalprojectCSCI1430/stencils/back/arrow_b.jpeg')

image = 'finalprojectCSCI1430/colorLocator/results/left (2)/all.jpeg'

sift.get_SIFT_features(image)
sift.show_SIFT_features()
