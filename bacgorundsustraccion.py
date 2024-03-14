import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 10)

camBackGround = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    # Lee un fotograma de la cámara
    ret, frame = cam.read()
    
    backGround = camBackGround.apply(frame)

    cv2.imshow("fondo", backGround)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cam.release()

cv2.destroyAllWindows()