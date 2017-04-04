from subprocess import call
import numpy as np
import cv2
import math


def sortByArea(cnts): 
    best_cnt = 0
    max_area = 0
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    return  best_cnt  

def magic(thresh):
    st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
    st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10), (4, 4))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, st1) 
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    return thresh

def centre(cnt):
    M = cv2.moments(cnt)
    cx,cy =int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(img,(cx,cy),10,255,-1)
    return cx,cy


cap = cv2.VideoCapture(0)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 10) 

# load the games image
#img = cv2.imread("1.jpg")
ret, img = cap.read()
mupper = np.array([35,255,255])   #yellow mark
mlower = np.array([15,90,180])

bupper = np.array([103,255,255])      #blue bot
blower = np.array([87,90,90])

rupper = np.array([190,255,255])  #red target
rlower = np.array([165,120,100])

#bupper = np.array([115,255,255])      #oldblue
#blower = np.array([95,110,90])

rx=ry=mx=my=bx=by=0
mxold=myold=bxold=byold= -1


while(True):
    ret, img = cap.read()
    
                    #step one
    blur = cv2.blur(img,(5,5))
#hsv
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV )
#color
    rthresh = cv2.inRange(hsv, rlower, rupper)
    bthresh = cv2.inRange(hsv, blower, bupper)
    mthresh = cv2.inRange(hsv, mlower, mupper)

    cv2.imshow("Image1", img)
    cv2.imshow("Image2", mthresh)
    cv2.waitKey(200)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
        
        

