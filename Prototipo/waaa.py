import cv2
import numpy as np

# Detecta las esquinas en la imagen
gray = cv2.imread("fotoaaa.png", cv2.IMREAD_GRAYSCALE)
corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)

# Coordenadas de la esquina de referencia
ref_corner = (100, 100)  # Por ejemplo, una esquina predeterminada

# Calcula la distancia euclidiana entre cada esquina detectada y la esquina de referencia
distances = [(np.linalg.norm(corner - ref_corner), corner) for corner in corners.reshape(-1, 2)]

# Ordena las esquinas por distancia
distances.sort()

# La esquina más cercana a la esquina de referencia se considera la misma esquina
reference_corner = distances[0][1]

# Ahora puedes trabajar con la esquina de referencia
print("Esquina de referencia:", reference_corner)

