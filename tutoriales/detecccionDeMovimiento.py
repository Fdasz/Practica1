import cv2
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 10)

camBackGround = cv2.bgsegm.createBackgroundSubtractorMOG()



while True:
    # Lee un fotograma de la cámara
    ret, frame = cam.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )
    backGround = camBackGround.apply(gray)
    cv2.rectangle(frame , (0,0), (frame.shape[1],40), (0,0,0), -1)
    color = (0, 255 ,0)
    textoEstado = "MovimientoDetectado: NO"

    areaCuadrado = np.array([[50,320],[620,320],[620,200],[50,200]])

    mascara = np.zeros(shape=(frame.shape[:2]),dtype=np.uint8)
    mascara = cv2.drawContours(mascara,[areaCuadrado],-1, (255), -1)
    mascara = cv2.bitwise_and(gray,gray,mask=mascara)

    fgmascara = camBackGround.apply(mascara)

    cnts =  cv2.findContours(fgmascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 500:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            textoEstado = "MovimientoDetectado: SI"

    cv2.drawContours(frame, [areaCuadrado], -1, color)
    cv2.putText(frame, textoEstado, (10,30), cv2.FONT_HERSHEY_SIMPLEX , 1 , color, 2)
    

    cv2.imshow("mask", fgmascara)
    cv2.imshow("original",frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cam.release()

cv2.destroyAllWindows()