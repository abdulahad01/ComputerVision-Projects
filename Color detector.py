def nothing (x) :
    pass



import cv2
import numpy as np

cap = cv2.VideoCapture(-1)
cap.set(3, 480)
cap.set (4,600)

cv2.namedWindow('task')
cv2.createTrackbar('L-H','task',0,179,nothing)
cv2.createTrackbar('L-S','task',0,255,nothing)
cv2.createTrackbar('L-V','task',0,255,nothing)

cv2.createTrackbar('U-H','task',0,179,nothing)
cv2.createTrackbar('U-S','task',0,255,nothing)
cv2.createTrackbar('U-V','task',0,255,nothing)

cv2.createTrackbar('frame/hsv/gray','task',0,2,nothing)
while True :
    ret , frame = cap.read()
    #cv2.imshow('drake', frame)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    H =cv2.getTrackbarPos('U-H','task')
    S =cv2.getTrackbarPos('U-S','task')
    V =cv2.getTrackbarPos('U-V','task')
    h =cv2.getTrackbarPos('L-H','task')
    s =cv2.getTrackbarPos('L-S','task')
    v =cv2.getTrackbarPos('L-V','task')
    s = cv2.getTrackbarPos('frame/hsv/gray','task')

    upper_blue = np.array([H,S,V ])
    lower_blue = np.array([h,s,v ])

   
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
   

    #print(b,g,r)
    #frame[:] = [b,g,r] 


    
    res = cv2.bitwise_and(frame,hsv, mask= mask)
    cv2.imshow('frame', frame)
    cv2.imshow('hsv', mask)
    cv2.imshow('result', res)
    if cv2.waitKey(1) & 0xFF ==ord('q') :
        break
    

cap.release()
cv2.destroyAllWindows()
    
