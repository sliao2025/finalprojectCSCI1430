import cv2 
import numpy as np

from scipy.spatial.distance import pdist
sift = cv2.SIFT_create()

#feature matching
class SIFT:
    def __init__(self,cross:str,star:str,arrow_f:str,arrow_b:str) -> None:
        self.cross = cv2.imread(cross)  
        self.star = cv2.imread(star)
        self.arrow_f = cv2.imread(arrow_f)
        self.arrow_b = cv2.imread(arrow_b)
        self.output_img = None
    
    def show_SIFT_features(self):   
        cv2.imshow('SIFT', self.output_img)
        cv2.waitKey(0)
    
    def get_SIFT_features(self,image):
        #create matcher
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        
        img = cv2.imread(image)
        red = img[:,:,2] #cross or star
        green = img[:,:,1] #arrow front
        blue = img[:,:,2] #arrow back
        # red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        
        keypoints_cross, descriptors_cross = sift.detectAndCompute(self.cross,None)
        keypoints_star, descriptors_star = sift.detectAndCompute(self.star,None)
        keypoints_red, descriptors_red = sift.detectAndCompute(red,None)

        #Get matches between the red symbol and cross
        matches_c = bf.match(descriptors_cross,descriptors_red)
        matches_c = sorted(matches_c, key = lambda x:x.distance)

        #Get matches between red symbol and star
        matches_s = bf.match(descriptors_star,descriptors_red)
        matches_s = sorted(matches_s, key = lambda x:x.distance)

        # Get the indices of the matching keypoints
        matches_red_c = [match.trainIdx for match in matches_c]
        matches_red_s = [match.trainIdx for match in matches_s]

        # Get the coordinates of the matching keypoints
        matches_red_c_coords = [keypoints_red[idx].pt for idx in matches_red_c]
        matches_red_s_coords = [keypoints_red[idx].pt for idx in matches_red_s]

        #Get the average distance of the matches in the red image
        avg_distances_red_c = np.mean(pdist(matches_red_c_coords))
        avg_distances_red_s = np.mean(pdist(matches_red_s_coords))
        
        print(avg_distances_red_c,avg_distances_red_s)
        if avg_distances_red_c < avg_distances_red_s:
            #it's a cross, test for up and left directions
            # green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
            keypoints_arrow_f, descriptors_arrow = sift.detectAndCompute(self.arrow_f,None)
            keypoints_green, descriptors_green = sift.detectAndCompute(green,None)

            matches = bf.match(descriptors_arrow,descriptors_green)
            matches = sorted(matches, key = lambda x:x.distance)

            # Get the indices of the matching keypoints in the green channel
            matches_green = [match.trainIdx for match in matches]

            # Get the coordinates of the matching keypoints in the green channel
            matches_green_coords = [keypoints_green[idx].pt for idx in matches_green]

            # Get the average coordinates of the matching keypoints in the green channel
            avg_coords_green = np.mean(matches_green_coords,axis=0)
            avg_coords_red_c = np.mean(matches_red_c_coords,axis=0)

            if(abs(avg_coords_green[0]-avg_coords_red_c[0]) > abs(avg_coords_green[1]-avg_coords_red_c[1])):
                #arrow to the left of the cross
                #move mouse to the left
                x=1
            else:
                x=0
                #arrow above the cross
                #move mouse up

        else:
            #it's a star, test for down and right directions 
            keypoints_arrow_b, descriptors_arrow = sift.detectAndCompute(self.arrow_b,None)


        #convert to grayscale
        
        # arrow = cv2.cvtColor(arrow, cv2.COLOR_BGR2GRAY)
        # squiggle = cv2.cvtColor(squiggle, cv2.COLOR_BGR2GRAY)

        self.output_img = cv2.drawMatches(self.star, keypoints_star, red, keypoints_red, matches_c[0:10], None, flags=2)



 