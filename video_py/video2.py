import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('D:/AI/OpenCV/data/haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        img = cv2.flip(img,1)
        cv2.imshow('img',img)
    if cv2.waitKey(1) &0xFF == ord(' '):  #按空格键退出
            break
cap.release()
cv2.destroyAllWindows()