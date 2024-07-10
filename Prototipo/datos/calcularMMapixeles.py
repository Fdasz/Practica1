

def mostrarDatos():
    
    # Leer el archivo y extraer los datos
    with open('datosModa.txt', 'r') as file:
        lines = file.readlines()

    # Separar los datos de posición y tiempo
    posiciones = []
    a = open('datosTransformados.txt','w')
    a.close()
    # Procesar las líneas para extraer tiempo en segundos y posición
    for line in lines:
        parts = line.split()

        try:
            distancia = float(parts[4])

            posiciones.append(distancia)

            with open('datosTransformados.txt', 'a') as archivo:
                archivo.write(f"{parts[0]} {parts[1]} {parts[2]} {parts[3]} {parts[4]} {parts[5]} {distancia*0.25} \n")

        
        except Exception as e:
            print(f"Error al procesar la línea: {line}. Error: {e}")
            continue


mostrarDatos()
    