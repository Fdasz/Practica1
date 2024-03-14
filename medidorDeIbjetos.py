import numpy as np
import cv2

#DEFINICION ARUCO
parametros = cv2.aruco.DetectorParameters()
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

#COLORES
LowAzul = np.array([96,144,106], np.uint8)
HighAzul = np.array([124,255,255], np.uint8)

LowVerde = np.array([43,52,106], np.uint8)
HighVerde = np.array([91,255,255], np.uint8)

LowRojo1 = np.array([0,100,20], np.uint8)
HighRojo1 = np.array([10,255,255], np.uint8)
LowRojo2 = np.array([175,100,20], np.uint8)
HighRojo2 = np.array([180,255,255], np.uint8)

def auxNada(x):
    pass

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:

        frame = cv2.resize(frame, (650,550))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #FUNCION DE MEDIDAS
        def medir(contorno, cap):
            for c in contorno:
                area = cv2.contourArea(c)
                if area > 2000:
                    rectangulo = cv2.minAreaRect(c)
                    (x, y), (an, al), angulo = rectangulo

                    ancho = an / proporcion_cm
                    alto = al / proporcion_cm
                        
                    #cv2.circle(cap, (int(x), int(y)), 5, (255,255,0), -1)

                    rect = cv2.boxPoints(rectangulo)
                    rect = np.int0(rect)

                    cv2.polylines(cap, [rect], True, (0,255,255), 2)

                    cv2.putText(cap, 'Ancho: {} cm'.format(round(ancho, 1)), (int(x), int(y-15)), cv2.LINE_AA, 0.8, (150, 0, 255), 2)
                    cv2.putText(cap, 'Alto: {} cm'.format(round(alto, 1)), (int(x), int(y+15)), cv2.LINE_AA, 0.8, (75, 0, 75), 2)

        #ARUCO
        esquinas, ids, _ = cv2.aruco.detectMarkers(frame, diccionario, parameters = parametros)

        #ASEGURAMOS QUE EL ARUCO SEA DETECTADO
        if np.all(ids != None):
            esquinasInt = np.int0(esquinas)
            cv2.polylines(frame, esquinasInt, True, (0,0,255),2)

            per_Aruco = cv2.arcLength(esquinasInt[0], True)
            proporcion_cm = per_Aruco / 13

            #MASCARAS
            maskAzul = cv2.inRange(hsv, LowAzul, HighAzul)
            maskVerde = cv2.inRange(hsv, LowVerde, HighVerde)
            maskRojo1 = cv2.inRange(hsv, LowRojo1, HighRojo1)
            maskRojo2 = cv2.inRange(hsv, LowRojo2, HighRojo2)

            #CONTORNOS
            contornoAzul, _ = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornoVerde, _ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornoRojo1, _ = cv2.findContours(maskRojo1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornoRojo2, _ = cv2.findContours(maskRojo2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #MEDIDAS
            medir(contornoAzul, frame)
            medir(contornoVerde, frame)
            medir(contornoRojo1, frame)
            medir(contornoRojo2, frame)
        
        #MOSTRAR VIDEO
        cv2.imshow('Live', frame)

        k = cv2.waitKey(5)
        if k == 27:
           cv2.destroyAllWindows()
           cap.release()