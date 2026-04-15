import jpype
import jpype.imports
import os
import time
from tests_logger import setup_logging

# Inicializamos el log antes de cualquier otra cosa
setup_logging("log_ejecucion_jpype.log")


# 1. Preparación (Fuera del cronómetro)
jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jar_path])

from matrixmath import Matrix, MatrixDet


def format_matrix(data):
    """Convierte un JArray de Java en una cadena visual bonita."""
    return "\n" + "\n".join([str([round(float(v), 3) for v in fila]) for fila in data])


def ejecutar_logica_calculo(matriz_datos, servicio, iter=0):
    # Crear objeto Java
    m_java = Matrix(matriz_datos)
    m_java.printMatrix()
    # Devolver matriz desde Java para mostrarla formateada en Python
    matriz_raw = m_java.getData()
    if iter == 0:
        print(f"Matriz formateada en Python: {format_matrix(matriz_raw)}")

    # Cálculos y prints
    det = servicio.calculateDeterminant(m_java)
    if iter == 0:
        print(f"Determinante: {det}")

    if servicio.isInvertible(m_java):
        if iter == 0:
            print("La matriz es invertible.")
        inv = servicio.calculateInverse(m_java)
        for fila in inv.getData():
            if iter == 0:
                print([round(float(v), 3) for v in fila])
    else:
        if iter == 0:
            print("No es invertible.")


if __name__ == "__main__":
    # Datos de prueba (Matriz C)

    A = [[1, 2], [1, 4]]  # invertible
    B = [[1.0, -1.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0]]  # invertible
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    D = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # no invertible
    servicio = MatrixDet()

    n_ejecuciones = 10
    tiempos = []
    print("===" * 12)
    print(
        f"Prueba con matriz C determinante e inversa con {n_ejecuciones} ejecuciones (JPype)"
    )
    for i in range(n_ejecuciones):
        inicio = time.time()

        ejecutar_logica_calculo(C, servicio, iter=i)

        tiempos.append(time.time() - inicio)

    print(f"\nPROMEDIO JPYPE: {sum(tiempos)/n_ejecuciones:.6f} segundos")
    print("===" * 12)
