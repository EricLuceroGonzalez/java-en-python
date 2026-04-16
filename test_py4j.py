from py4j.java_gateway import JavaGateway, GatewayParameters
import time
import random
from tests_logger import setup_logging

# Inicializamos el log antes de cualquier otra cosa
setup_logging("log_ejecucion_py4j.log")
# setup_logging("log_ejecucion_py4j_10x10.log")


def python_to_java_double_array(gateway, data):
    filas, columnas = len(data), len(data[0])
    java_array = gateway.new_array(gateway.jvm.double, filas, columnas)
    for i in range(filas):
        for j in range(columnas):
            java_array[i][j] = float(data[i][j])
    return java_array


def ejecutar_logica_calculo(matriz_datos, app, gateway, iter=0):
    # RELOJ: Inicio del socket
    t_ini_socket = time.perf_counter()
    # Convertir datos y crear objeto
    java_array = python_to_java_double_array(gateway, matriz_datos)
    m_java = app.createMatrix(java_array)
    t_fin_socket = time.perf_counter()

    # Ojo: se imprime en consola Java, no en Python, por eso el print() es del objeto Java/
    matriz_python = m_java.getData()

    # Obtener servicio
    servicio = app.getService()

    # RELOJ: Inicio del cálculo puro en Java
    t_ini_calculo = time.perf_counter()
    # Cálculos y prints (Exactamente igual que en JPype)
    det = servicio.calculateDeterminant(m_java)
    # print(f"Iteración {iter+1}: Determinante = {det:.16f}")

    if servicio.isInvertible(m_java):
        inv = servicio.calculateInverse(m_java)

    t_fin_calculo = time.perf_counter()
    # Resultados segmentados
    t_socket = t_fin_socket - t_ini_socket
    t_algoritmo = t_fin_calculo - t_ini_calculo
    return t_socket, t_algoritmo


if __name__ == "__main__":
    t_total_ini = time.perf_counter()
    # 1. Conexión inicial (Se hace UNA SOLA VEZ)
    gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
    app = gateway.entry_point

    A = [[1, 2], [1, 4]]  # invertible
    B = [[1.0, -1.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0]]  # invertible
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    D = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # no invertible
    dimension = 10
    matriz_10x10 = [
        [round(random.randint(-10, 10), 2) for _ in range(dimension)]
        for _ in range(dimension)
    ]
    matriz_10x10 = [
        [-4.0, -9.0, -1.0, 6.0, 9.0, 4.0, -3.0, 4.0, 4.0, -4.0],
        [2.0, 4.0, -9.0, -7.0, 8.0, -5.0, 6.0, -9.0, 1.0, 4.0],
        [-1.0, -6.0, 0.0, 4.0, -5.0, 8.0, 9.0, 1.0, -5.0, 7.0],
        [-6.0, -8.0, 5.0, -6.0, 9.0, 6.0, 7.0, 5.0, 6.0, 9.0],
        [2.0, 8.0, -5.0, 0.0, 8.0, -2.0, -5.0, 7.0, -5.0, 1.0],
        [1.0, -6.0, 0.0, -3.0, -3.0, -4.0, -5.0, -7.0, -2.0, 7.0],
        [-4.0, 6.0, 6.0, -4.0, 3.0, 2.0, -3.0, 2.0, 2.0, -5.0],
        [0.0, 7.0, -2.0, -5.0, 0.0, -7.0, 8.0, 5.0, -5.0, -6.0],
        [-6.0, 0.0, -3.0, -1.0, 1.0, 6.0, 8.0, -4.0, -2.0, -8.0],
        [-2.0, -9.0, 3.0, -1.0, 3.0, 4.0, -5.0, -4.0, -5.0, -7.0],
    ]
    # matrix = matriz_10x10
    matrix = C
    n_ejecuciones = 5
    tiempos_socket = []
    tiempos_algo = []
    print("===" * 12)
    print(
        f"Prueba con matriz 3x3, determinante e inversa con {n_ejecuciones} ejecuciones (PY4J)"
        # f"Prueba con matriz C, determinante e inversa con {n_ejecuciones} ejecuciones (PY4J)"
    )
    for i in range(n_ejecuciones):
        t_socket, t_algo = ejecutar_logica_calculo(matrix, app, gateway, iter=i)
        tiempos_socket.append(t_socket)
        tiempos_algo.append(t_algo)
    t_total_fin = time.perf_counter()
    t_total = t_total_fin - t_total_ini
    print(f"\nPROMEDIO SOCKET: {sum(tiempos_socket)/n_ejecuciones:.6f} segundos")
    print(f"\nPROMEDIO ALGORITMO: {sum(tiempos_algo)/n_ejecuciones:.6f} segundos")
    print(f"\nTIEMPO TOTAL: {t_total:.6f} segundos")
    print("===" * 12)
