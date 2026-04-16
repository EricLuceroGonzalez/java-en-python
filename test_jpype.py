import random
import jpype
import jpype.imports
import os
import time
from tests_logger import setup_logging

# Inicializamos el log antes de cualquier otra cosa
setup_logging("log_ejecucion_jpype.log")
# setup_logging("log_ejecucion_jpype_10x10.log")


# 1. Preparación (Fuera del cronómetro)
jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jar_path])

from matrixmath import Matrix, MatrixDet


def format_matrix(data):
    """Convierte un JArray de Java en una cadena visual legible."""
    return "\n" + "\n".join([str([round(float(v), 3) for v in fila]) for fila in data])


def ejecutar_logica_calculo(matriz_datos, servicio, iter=0):
    # Crear objeto Java
    t_ini_java = time.perf_counter()
    m_java = Matrix(matriz_datos)
    t_fin_java = time.perf_counter()

    # Devolver matriz desde Java para mostrarla formateada en Python
    # m_java.printMatrix()
    matriz_raw = m_java.getData()

    # Cálculos y prints
    t_ini_algo = time.perf_counter()
    det = servicio.calculateDeterminant(m_java)
    if servicio.isInvertible(m_java):
        inv = servicio.calculateInverse(m_java)

    t_fin_algo = time.perf_counter()
    # Resultados de tiempo segmentados
    t_java = t_fin_java - t_ini_java
    t_algoritmo = t_fin_algo - t_ini_algo
    return t_java, t_algoritmo


if __name__ == "__main__":
    t_total_ini = time.perf_counter()
    # Datos de prueba (Matriz C)
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
    servicio = MatrixDet()
    matrix = C
    n_ejecuciones = 5
    tiempos_java = []
    tiempos_algoritmo = []
    print("===" * 12)
    print(
        # f"Prueba con matriz 10x10, determinante e inversa con {n_ejecuciones} ejecuciones (JPype)"
        f"Prueba con matriz 3x3 determinante e inversa con {n_ejecuciones} ejecuciones (JPype)"
    )
    for i in range(n_ejecuciones):

        t_java, t_algoritmo = ejecutar_logica_calculo(matrix, servicio, iter=i)
        tiempos_java.append(t_java)
        tiempos_algoritmo.append(t_algoritmo)
    t_total_fin = time.perf_counter()
    t_total = t_total_fin - t_total_ini
    print(f"\nPROMEDIO JAVA: {sum(tiempos_java)/n_ejecuciones:.6f} segundos")
    print(f"PROMEDIO ALGORITMO: {sum(tiempos_algoritmo)/n_ejecuciones:.6f} segundos")
    print(f"TIEMPO TOTAL: {t_total:.6f} segundos")
    print("===" * 12)
