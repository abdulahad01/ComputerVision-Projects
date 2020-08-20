import cv2
import numpy as np
import time

#Load the camera
time.sleep(3)
cap = cv2.VideoCapture(0)
print("Opening Camera ... ")
for i in range (60):
    _,background = cap.read()

background = np.flip(background, axis  = 1)
    
while cap.isOpened() :
    ret,frame = cap.read()
    
    if ret ==False :
        print("There seems to a problem with the camera")
        break
    else :
       
        frame = np.flip(frame , axis = 1)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #converting rgb color space to hsv 

        #values for custom color
        lower = np.array([86,69,27])
        upper = np.array([118,162,237])
        
        mask1 = cv2.inRange(hsv,lower,upper)
        
        #Mask erosion and dilation
        print("creating magic~!")
        kernel =np.ones([3,3],np.uint8)
        mask1= cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel) 
        mask1= cv2.morphologyEx(mask1, cv2.MORPH_DILATE, kernel)
        mask2 = cv2.bitwise_not(mask1) 

        res1 = cv2.bitwise_and(background, background, mask = mask1) #colored part
        res2 = cv2.bitwise_and(frame, frame, mask = mask2)          #Everything outside the color
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 

        #Display output
        print("Displaying output..")
        cv2.imshow("frame",final_output)  
        if cv2.waitKey(1) == 27 :
            break
cv2.destroyAllWindows()
cap.release()
    
