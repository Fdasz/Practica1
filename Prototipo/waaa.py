espacioGrilla = 10
pxm = 0

def pixelsxmilimetros(d):
    global espacioGrilla, pxm
    pxm = espacioGrilla/d
    return pxm


ancho = pixelsxmilimetros(50)
print(ancho)