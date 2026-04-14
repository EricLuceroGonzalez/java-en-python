from py4j.java_gateway import JavaGateway, GatewayParameters
import time


def python_to_java_double_array(gateway, data):
    filas, columnas = len(data), len(data[0])
    java_array = gateway.new_array(gateway.jvm.double, filas, columnas)
    for i in range(filas):
        for j in range(columnas):
            java_array[i][j] = float(data[i][j])
    return java_array


def ejecutar_logica_calculo(matriz_datos, app, gateway):
    # Convertir datos y crear objeto
    java_array = python_to_java_double_array(gateway, matriz_datos)
    m_java = app.createMatrix(java_array)
    # Ojo: se imprime en consola Java, no en Python, por eso el print() es del objeto Java/
    m_java.print()

    # Obtener servicio
    servicio = app.getDetService()

    # Cálculos y prints (Exactamente igual que en JPype)
    det = servicio.calculateDeterminant(m_java)
    print(f"Determinante: {det}")

    if servicio.isInvertible(m_java):
        print("La matriz es invertible.")
        inv = servicio.calculateInverse(m_java)
        for fila in inv.getData():
            print([round(float(v), 3) for v in fila])
    else:
        print("No es invertible.")


if __name__ == "__main__":
    # 1. Conexión inicial (Se hace UNA SOLA VEZ)
    gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
    app = gateway.entry_point

    A = [[1, 2], [1, 4]]  # invertible
    B = [[1.0, -1.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0]]  # invertible
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    D = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # no invertible

    n_ejecuciones = 10
    tiempos = []

    for i in range(n_ejecuciones):
        print(f"\n--- Iteración {i+1} (Py4J) ---")
        inicio = time.time()

        ejecutar_logica_calculo(C, app, gateway)

        tiempos.append(time.time() - inicio)

    print(f"\nPROMEDIO PY4J: {sum(tiempos)/n_ejecuciones:.6f} seg")
