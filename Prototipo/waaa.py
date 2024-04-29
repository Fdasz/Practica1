espacioGrilla = 10
pxm = 0

def pixelsxmilimetros(d):
    global espacioGrilla, pxm
    pxm = espacioGrilla/d
    return pxm

def calcularMM(d):
    global pxm
    mm = pxm * d
    return mm


pixelsxmilimetros(50)
ancho = calcularMM(545)
print(ancho)
