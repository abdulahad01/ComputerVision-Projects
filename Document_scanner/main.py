import utils
import cv2

path = 'resources/test.jpeg'

utils.initialize_trackbar()
while True :
    t1,t2 =utils.get_val()
    # print(t1,t2)

    #Load Image
    img = cv2.imread(path)
    # print(img.shape)

    #Perform edge detection,dilation and erosion
    pp_img,orig_copy= utils.preprocess(img,t1,t2)
    imgContours=orig_copy.copy() #Copying image for display purposes

    #Finding contours from the binary image
    contours =utils.get_contours(pp_img)
    biggest_contours =utils.getBigCntr(contours)
    cv2.drawContours(imgContours,contours, -1, (0, 255, 0),2)
    reorderd_points = utils.reorder(biggest_contours)
    # print("reordered points : ",len(reorderd_points),type(reorderd_points))

    #Apply perspective transform on the resized image
    corrected =utils.get_perspective(reorderd_points,orig_copy)

    #Applying adaptive threshold
    gray = cv2.cvtColor(corrected,cv2.COLOR_BGR2GRAY)
    final = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    #display the images
    cv2.imshow("Image", orig_copy)
    cv2.imshow("Preprocessed", pp_img)
    cv2.imshow("contours" ,imgContours)
    cv2.imshow("Perspective corrected",corrected)
    cv2.imshow("Final",final)

    if cv2.waitKey(1) == 27 :
	#Save the output images
        cv2.imwrite("output/resized.jpeg",orig_copy)
        cv2.imwrite("output/preprocessed.jpeg",pp_img)
        cv2.imwrite("output/contours.jpeg", imgContours)
        cv2.imwrite("output/corrected.jpeg",corrected)
        cv2.imwrite("output/final.jpeg", final)
        break
cv2.destroyAllWindows()