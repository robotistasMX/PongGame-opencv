import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)

def nothing(x):
    pass

#Creamos una ventana llamada 'image' en la que habra todos los sliders
cv.namedWindow('image')
cv.createTrackbar('Hue Minimo','image',0,255,nothing)
cv.createTrackbar('Hue Maximo','image',0,255,nothing)
cv.createTrackbar('Saturation Minimo','image',0,255,nothing)
cv.createTrackbar('Saturation Maximo','image',0,255,nothing)
cv.createTrackbar('Value Minimo','image',0,255,nothing)
cv.createTrackbar('Value Maximo','image',0,255,nothing)

while(True):
    _ , frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hMin = cv.getTrackbarPos('Hue Minimo','image')
    hMax = cv.getTrackbarPos('Hue Maximo','image')
    sMin = cv.getTrackbarPos('Saturation Minimo','image')
    sMax = cv.getTrackbarPos('Saturation Maximo','image')
    vMin = cv.getTrackbarPos('Value Minimo','image')
    vMax = cv.getTrackbarPos('Value Maximo','image')

    lower_blue = np.array([hMin,sMin,vMin])
    upper_blue = np.array([hMax,sMax,vMax])

    mask = cv.inRange(hsv, lower_blue,upper_blue )

    filtro1 = cv.erode(mask, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filtro2 = cv.erode(filtro1, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)

    objct = cv.moments(filtro2)
    if objct['m00'] > 50000:
        cx = int(objct['m10']/objct['m00'])
        cy = int(objct['m01']/objct['m00'])
        cv.circle(frame, (cx,cy), 10, (0,0,255), 4)

    cv.imshow('original', frame)
    cv.imshow('azul', filtro2)
    k = cv.waitKey(5)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()
