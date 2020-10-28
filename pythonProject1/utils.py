import cv2
import numpy as np


def initialize_trackbar():
    def nothing(x):
        pass
    cv2.namedWindow("controls")
    cv2.createTrackbar("min threshold",'controls',6,255,nothing)
    cv2.createTrackbar("max threshold",'controls',39,255,nothing)

def get_val():
    t_min = cv2.getTrackbarPos("min threshold",'controls')
    t_max = cv2.getTrackbarPos("max threshold","controls")
    # print(t_max,t_min)
    return t_min,t_max


def preprocess (img,t1,t2) :
    r =int(img.shape[0]/614)
    dims = (img.shape[1]*r,614)
    img = cv2.resize(img,dims)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur =cv2.GaussianBlur(gray,(5,5),-1)
    canny = cv2.Canny(blur,t1,t2)
    imgDial = cv2.dilate(canny,(5,5), iterations=2)
    imageErode=cv2.erode(imgDial,(5,5),iterations=1)
    return imageErode,img

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4,2), dtype=np.int32)
    #top left pt has smallest sum and bottom right has largest sum and same analogy for diff
    sum = myPoints.sum(axis=1)
    myPointsNew[0] = myPoints[np.argmin(sum)]
    myPointsNew[2] =myPoints[np.argmax(sum)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[3] = myPoints[np.argmax(diff)]

    return myPointsNew

def getBigCntr(cntr):
    bigcnt = np.array([])
    for cnt in (cntr):
        perimeter = cv2.arcLength(cnt, True)

        epsilon = 0.1 * perimeter
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        # print("approx :",len(approx))
        if len(approx) == 4 :
            bigcnt = approx
            break
            #print("Biggest contours are : ",bigcnt)
    return bigcnt

def get_contours(img):
    contrs,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # print("The biggest contour detected is ",(cntrs))
    sorted_contours = sorted(contrs,key=cv2.contourArea,reverse=True)[:5]
    return sorted_contours


def get_perspective(contrs,orig) :
    width=int(orig.shape[1])
    height = int(orig.shape[0])
    # print(len(contrs))
    pts1 = np.float32(contrs)
    # print(pts1)
    pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])
    matrix =cv2.getPerspectiveTransform(pts1,pts2)
    result = cv2.warpPerspective(orig,matrix,(width,height))
    return result
