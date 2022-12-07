#https://pysource.com/2018/05/14/optical-flow-with-lucas-kanade-method-opencv-3-4-with-python-3-tutorial-31/

import cv2
import numpy as np
from PIL import Image


#ENTER YOUR NAME FOR SAVING PURPOSES

USER_NAME = "Edrick"

#*************************************










cap = cv2.VideoCapture(0)

# Create old frame
_, frame = cap.read()
#convert frame to gray
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Lucas kanade params
window_size = (15,15)

# lk_params = dict(winSize = window_size,
# maxLevel = 4,
# criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


calibrate_points = []

# Mouse function
def select_point(event, x, y, flags, params):
    global point, point_selected, old_points, calibrate_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        
        if len(calibrate_points) == 1:
            calibrate_points.append(point)
            first_point = calibrate_points[0]
            second_point = calibrate_points[1]
            #calculate center from two points
            center_x = (first_point[0] + second_point[0])//2
            center_y = (first_point[1] + second_point[1])//2
            old_points = np.array([[center_x, center_y]], dtype=np.float32)
            point = (center_x, center_y)
        elif len(calibrate_points) == 2:
            calibrate_points = []
            calibrate_points.append(point)
        else:
            calibrate_points.append(point)

        point_selected = True
        

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)

point_selected = False
point = ()
old_points = np.array([[]])


x = 0
y = 0
x_length = 0
y_length = 0

not_capturing = True

gestures = ["click", "left", "right", "up"]
num_images = [0, 0, 0, 0]


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    key = cv2.waitKey(1)
    testkeyPressed = key==51 or key == 52 or key == 53 or key ==54
    if key == 50:
        break
    elif testkeyPressed == True:
        not_capturing = False

    if not_capturing == True:
        for cal_point in calibrate_points:
            cv2.circle(frame, cal_point, 2, (0, 0, 255), 2)
    
    if len(calibrate_points) == 2:
        #cv2.circle(frame, point, 100, (0, 0, 255), 2)

        first = calibrate_points[0]
        second = calibrate_points[1]

        x_length = abs(second[0] - first[0])
        y_length = abs(second[1] - first[1])

        window_size = (x_length, y_length)

        lk_params = dict(winSize = window_size,
        maxLevel = 4,
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.05))

        
        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        old_gray = gray_frame.copy()
        old_points = new_points

        x, y = new_points.ravel()
        
        #cv2.circle(frame, (int(x), int(y)), 100, (0, 255, 0), -1)

        #first      second      window_size
        #(10,15) - (20, 30) -> (10, 15)
        #(15,22.5) left (minus x  plus y) right (plus x minus y)
        

       

        # center_x = (first[0] + second[0])//2
        # center_y = (first[1] + second[1])//2

        #cv2.rectangle(frame, (first[0],first[1]), (second[0],second[1]),(0, 255, 0), 2)

        if not_capturing == True:
            cv2.rectangle(frame, (int(x - (x_length //2)), int(y + (y_length//2))), (int(x + (x_length//2)), int(y - (x_length//2))),(0, 255, 0), 2)

        #cv2.circle(frame, (int(x), int(y)), 100, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    if testkeyPressed == True:
        frame_cut = frame[int(y - (y_length//2) - 10): int(y + (y_length//2) + 10),int(x - (x_length //2) - 10): int(x + (x_length//2) + 0), :]
        file_path = "./skinAlgorithm/trainingImages/{}/{}{}{}.jpg".format(gestures[(key % 50) - 1],USER_NAME, gestures[(key % 50) - 1], num_images[(key%50) - 1])
        cv2.imwrite(file_path, frame_cut)
        num_images[(key%50) - 1] += 1
        not_capturing = True
    

    



cap.release()
cv2.destroyAllWindows()