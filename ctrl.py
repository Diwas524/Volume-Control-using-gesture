import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

from pynput.keyboard import Key,Controller
keyboard = Controller()

################################
wCam, hCam = 1280, 720
################################
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
 
detector = htm.handDetector(detectionCon=0.7)


last_angle=None
last_length=None



minAngle = 0
maxAngle = 180
angle    = 0
angleBar = 400
angleDeg = 0
minHand  = 50 #50
maxHand  = 300 #300
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
 
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
 
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
 
        # Hand range 50 - 300
    
        angle  = np.interp(length, [minHand, maxHand], [minAngle, maxAngle])
        angleBar = np.interp(length, [minHand, maxHand], [400, 150])
        angleDeg = np.interp(length, [minHand, maxHand], [0, 180])   # degree angle 0 - 180
       

        if last_length:
            if length>last_length:
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
                print("VOL UP")
            elif length<last_length:
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
                print("VOL DOWN")
        
        last_angle=angle
        last_length=length

        # print(int(length), angle)
 
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
 
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(angleBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(angleDeg)} deg', (40, 90), cv2.FONT_HERSHEY_COMPLEX,
                2, (0, 9, 255), 3)
 
    cv2.imshow("Img", img)
    cv2.waitKey(1)