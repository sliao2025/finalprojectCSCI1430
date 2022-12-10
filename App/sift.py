import cv2 
import numpy as np

from scipy.spatial.distance import pdist
sift = cv2.SIFT_create()

#feature matching
class SIFT:
    def __init__(self,reference:str,arrow_f:str,arrow_b:str) -> None:
        self.reference = cv2.imread(reference)
        self.arrow_f = cv2.imread(arrow_f)
        self.arrow_b = cv2.imread(arrow_b)
        self.output_img = None
    
    def show_SIFT_features(self):   
        cv2.imshow('SIFT', self.output_img)
        cv2.waitKey(0)
    
    def get_SIFT_features(self,img):
        #create matcher
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        
        #img = cv2.imread(image)
        red = img[:,:,0] #cross or star
        green = img[:,:,1] #arrow front
        blue = img[:,:,2] #arrow back
        # red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        cv2.imshow('red',red)
        cv2.waitKey(0)
        cv2.imshow('green',green)
        cv2.waitKey(0)
        
        keypoints_ref, descriptors_ref = sift.detectAndCompute(self.reference,None)
        keypoints_red, descriptors_red = sift.detectAndCompute(red,None)

        #Get matches between reference image and red symbol
        matches = bf.match(descriptors_ref,descriptors_red)
        matches = sorted(matches,key=lambda x:x.distance)

        # Get the indices of the matching keypoints
        matches_red = [match.trainIdx for match in matches]
        matches_ref = [match.queryIdx for match in matches]


        # Get the coordinates of the matching keypoints
        matches_red = [keypoints_red[idx].pt for idx in matches_red]
        matches_ref = [keypoints_ref[idx].pt for idx in matches_ref]

        # Find the average x and y coordinates of the matches
        avg_x_red = np.mean([pt[0] for pt in matches_red])
        avg_y_red = np.mean([pt[1] for pt in matches_red])
        avg_x_ref = np.mean([pt[0] for pt in matches_ref])
        avg_y_ref = np.mean([pt[1] for pt in matches_ref])

        # Combine the average x and y coordinates into a tuple
        avg_coord_red = (avg_x_red, avg_y_red)
        avg_coord_ref = (avg_x_ref, avg_y_ref)
        print(avg_coord_red,avg_coord_ref)

        cross_diff = abs(avg_coord_ref[0] - 43.6)
        star_diff = abs(avg_coord_ref[0] - 117.6)
        
        if cross_diff < star_diff: #cross, test for up and left
            # green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
            keypoints_arrow_f, descriptors_arrow_f = sift.detectAndCompute(self.arrow_f,None)
            keypoints_green, descriptors_green = sift.detectAndCompute(green,None)

            matches_arrow = bf.match(descriptors_arrow_f,descriptors_green)
            matches_arrow = sorted(matches_arrow, key = lambda x:x.distance)

            # Get the indices of the matching keypoints in the green channel
            matches_green = [match.trainIdx for match in matches_arrow]

            # Get the coordinates of the matching keypoints in the green channel
            matches_green_coords = [keypoints_green[idx].pt for idx in matches_green]

            img = cv2.drawMatches(self.arrow_f, keypoints_arrow_f, green, keypoints_green, matches_arrow[0:10], None, flags=2)
            cv2.imshow('arrow',img)
            cv2.waitKey(0)
            # Get the average coordinates of the matching keypoints in the green channel
            avg_x_green = np.mean([pt[0] for pt in matches_green_coords])
            avg_y_green = np.mean([pt[1] for pt in matches_green_coords])
            print(avg_x_green,avg_y_green)

            if abs(avg_x_green-avg_x_red) > abs(avg_y_green-avg_y_red):
                #arrow to the left of the cross
                #move mouse to the left
                print('left')
            else:
                #arrow above the cross
                #move mouse up
                print('up')

        else:
            #it's a star, test for down and right directions 
            keypoints_arrow_b, descriptors_arrow_b = sift.detectAndCompute(self.arrow_b,None)
            keypoints_green, descriptors_green = sift.detectAndCompute(green,None)
            
            matches_arrow = bf.match(descriptors_arrow_b,descriptors_green)
            matches_arrow = sorted(matches_arrow, key = lambda x:x.distance)

            # Get the indices of the matching keypoints in the green channel
            matches_green = [match.trainIdx for match in matches_arrow]

            # Get the coordinates of the matching keypoints in the green channel
            matches_green_coords = [keypoints_green[idx].pt for idx in matches_green]

            img = cv2.drawMatches(self.arrow_b, keypoints_arrow_b, green, keypoints_green, matches_arrow[0:10], None, flags=2)
            cv2.imshow('arrow',img)
            cv2.waitKey(0)

           # Get the average coordinates of the matching keypoints in the green channel
            avg_x_green = np.mean([pt[0] for pt in matches_green_coords])
            avg_y_green = np.mean([pt[1] for pt in matches_green_coords])
            print(avg_x_green,avg_y_green)

            if abs(avg_x_green-avg_x_red) > abs(avg_y_green-avg_y_red):
                #arrow to the right of the cross
                #move mouse to the right
                print('right')
            else:
                #arrow below the cross
                #move mouse down
                print('down')

        self.output_img = cv2.drawMatches(self.reference, keypoints_ref, red, keypoints_red, matches[0:10], None, flags=2)



 