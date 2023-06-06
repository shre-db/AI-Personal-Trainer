import cv2 as cv
import numpy as np
import time
import pose_module as pm

cap = cv.VideoCapture(0)
detector = pm.PoseDetector()
count = 0
dire = 0
p_time = 0
while True:
    success, img = cap.read()
    img = detector.find_pose(img, False)
    lm_list = detector.find_position(img, False)
    if len(lm_list) != 0:
        # Left Arm
        angle = detector.find_angle(img, 11, 13, 15)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
        print(angle, per)

        # Check for the dumbbell curls
        if per == 100:
            if dire == 0:
                count += 0.5
                dire = 1
        if per == 0:
            if dire == 1:
                count += 0.5
                dire = 0

        print(count)

        cv.rectangle(img, (0,450), (250, 720), (0,255,0), cv.FILLED)

        cv.putText(img, f'{count}', (45, 670), cv.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 5)

    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time
    cv.putText(img, str(fps), (50, 100), cv.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)
    cv.imshow("Image", img)
    cv.waitKey(1)

