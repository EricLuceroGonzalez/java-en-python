import jpype
import jpype.imports
import os
import time

# 1. Preparación (Fuera del cronómetro)
jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jar_path])

from matrixmath import Matrix, MatrixDet


def ejecutar_logica_calculo(matriz_datos, servicio):
    # Crear objeto Java
    m_java = Matrix(matriz_datos)
    m_java.print_()

    # Cálculos y prints (Exactamente igual que en Py4J)
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
    # Datos de prueba (Matriz C)

    A = [[1, 2], [1, 4]]  # invertible
    B = [[1.0, -1.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0]]  # invertible
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    D = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # no invertible
    servicio = MatrixDet()

    n_ejecuciones = 10
    tiempos = []

    for i in range(n_ejecuciones):
        print(f"\n--- Iteración {i+1} (JPype) ---")
        inicio = time.time()

        ejecutar_logica_calculo(C, servicio)

        tiempos.append(time.time() - inicio)

    print(f"\nPROMEDIO JPYPE: {sum(tiempos)/n_ejecuciones:.6f} seg")
