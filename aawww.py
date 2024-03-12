import cv2
import numpy as np

# Inicializa la cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
while True:
    # Lee un fotograma de la cámara
    ret, frame = cap.read()

    # Convierte el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplica umbral adaptativo para detectar líneas
    _, thresh = cv2.threshold(gray, 0, 50, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Encuentra los contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Itera sobre los contornos
    for contour in contours:
        # Aproxima el contorno a un polígono
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Si el polígono tiene 4 vértices (un cuadrilátero)
        if len(approx) == 4:
            # Dibuja un rectángulo delimitador alrededor del cuadrilátero
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Muestra el fotograma
    cv2.imshow("Deteccion", frame)
    cv2.imshow("Deteccion2", gray)
    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
