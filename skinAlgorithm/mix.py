import cv2
import numpy as np


cap = cv2.VideoCapture(0)

# Create old frame
_, frame = cap.read()
#convert frame to gray
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Lucas kanade params
lk_params = dict(winSize = (15, 15),
maxLevel = 4,
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

calibrate_points = []


def select_point(event, x, y, flags, params):
    global point, point_selected, old_points, calibrate_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        if len(calibrate_points) == 2:
            calibrate_points = []
            old_points = np.array([[x, y]], dtype=np.float32)
        calibrate_points.append(point)
        # old_points = np.array([[x, y]], dtype=np.float32)


cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)

old_points = np.array([[]])
point = ()


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for cal_point in calibrate_points:
        cv2.circle(frame, cal_point, 2, (0, 0, 255), 2)

    if len(calibrate_points) == 2:

        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # first = calibrate_points[0]
        # second = calibrate_points[1]

        # lk_params = dict(winSize = ((second[0] - first[0]), (second[1] - first[1])),
        # maxLevel = 4,
        # criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        # old_gray = gray_frame.copy()
        # old_points = new_points
        # x, y = new_points.ravel()

        # cv2.rectangle(frame, first, second,(0, 255, 0), 2)

        cv2.circle(frame, point, 100, (0, 0, 255), 2)

        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        old_gray = gray_frame.copy()
        old_points = new_points

        x, y = new_points.ravel()
        
        #cv2.circle(frame, (int(x), int(y)), 100, (0, 255, 0), -1)

        cv2.rectangle(frame, (int(x - 50), int(y - 50)),  (int(x + 50), int(y + 50)),(0, 255, 0), 2)


    cv2.imshow("Frame", frame)


    key = cv2.waitKey(1)
    if key == 50:
        break


cap.release()
cv2.destroyAllWindows()
