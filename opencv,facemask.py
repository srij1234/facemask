
from time import sleep
# import pyvirtualcam
import cv2
import mediapipe as mp
import numpy as np
import subprocess
import os
import random
# sudoPassword = 'kaka1010'
# command = 'sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label="Virtual" exclusive_caps=1 max_buffers=2'
# p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
def nothing(x):
	pass
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
cap = cv2.VideoCapture(0)
cv2.namedWindow('controls')
cv2.createTrackbar('r','controls',0,255,nothing)
cv2.createTrackbar('b','controls',0,255,nothing)
cv2.createTrackbar('g','controls',0,255,nothing)
cv2.createTrackbar('mode','controls',0,2,nothing)

cv2.createTrackbar('edge','controls',0,6,nothing)
cv2.createTrackbar('z','controls',0,100,nothing)
cv2.createTrackbar('k','controls',0,2,nothing)
# with pyvirtualcam.Camera(width=640, height=480, fps=240, device='/dev/video4') as cam:

while True:
    _, image = cap.read()
    pqr=image
    height, width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = np.zeros((height,width,3), np.uint8)
    img[:,:] = (0,0,0)
    error=img
    z=cv2.getTrackbarPos('z','controls')
    thick=cv2.getTrackbarPos('edge','controls')-1
    result = face_mesh.process(image)
    x=cv2.getTrackbarPos('mode','controls')
    r=cv2.getTrackbarPos('r','controls')
    b=cv2.getTrackbarPos('b','controls')
    g=cv2.getTrackbarPos('g','controls')
    k=cv2.getTrackbarPos('k','controls')
    color=(r,g,b)
    if (x==0):
        try:
            for facial_landmarks in result.multi_face_landmarks:
                if(k==2):
                    r=random.randint(0,255)
                    g=random.randint(0,255)
                    b=random.randint(0,255)
                    color=(r,g,b)
                
                for i in range(0, 468):
                    if(k==1):
                        r=random.randint(0,255)
                        g=random.randint(0,255)
                        b=random.randint(0,255)
                        color=(r,g,b)
                    
                    pt1 = facial_landmarks.landmark[i]
                    x = int(pt1.x * width)
                    y = int(pt1.y * height)
                    pt2= facial_landmarks.landmark[i-1]
                    x1 = int(pt2.x * width)
                    y1 = int(pt2.y * height)
                    #cv2.line(img, (x,y) , (x1,y1), color,thick)
                    imS=cv2.circle(img, (x,y), z, color,thick)
        except :
            imS=error
    elif (x==2):
        imS=cv2.Canny(image,50,80)
        imS = cv2.cvtColor(imS, cv2.COLOR_GRAY2BGR)
        try:
            for facial_landmarks in result.multi_face_landmarks:
                for i in range(0, 468):
                    pt1 = facial_landmarks.landmark[i]
                    x = int(pt1.x * width)
                    y = int(pt1.y * height)
                    cv2.circle(imS, (x,y), z, color,thick)                        
        except :
            imS=error
    else:
        try:
            for facial_landmarks in result.multi_face_landmarks:
                for i in range(0, 468):
                    pt1 = facial_landmarks.landmark[i]
                    x = int(pt1.x * width)
                    y = int(pt1.y * height)
                    cv2.circle(img, (x,y), z,color,thick)
        except :
            imS=error
        imS=cv2.bitwise_not(img)
        image=cv2.bitwise_not(image)
        imS=cv2.bitwise_or(image,imS)
        imS=cv2.bitwise_not(imS)
        
    try:
        imS = cv2.flip(imS, 1)
    except:
        imS=error
    cv2.imshow("output", imS)
    # cam.send(imS)
    # cam.sleep_until_next_frame()
 
        
    key = cv2.waitKey(1)
   