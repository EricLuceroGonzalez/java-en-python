import jpype
import jpype.imports
from jpype.types import *
import os
import time

# Probamos jpype (https://github.com/jpype-project/jpype/)

# 1. Configuración de rutas
jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")

# 2. Inicio de la JVM
if not jpype.isJVMStarted():
    # El classpath apunta al JAR que compilamos con Maven
    jpype.startJVM(classpath=[jar_path])

# 3. Import de clases Java desde el .jar (/target) (ahora que la JVM está arriba)
from matrixmath import Matrix, MatrixService
from matrixmath import Main

# Probar el método main de Java (opcional, solo para verificar que se ejecuta sin errores)
Main.main([])


def probar_motor_java():
    # Definimos una matriz 3x3 o 2x2 que sabemos que tiene inversa (o no)
    matriz_en_main = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    A = [[1, 2], [1, 4]]  # invertible
    B = [[1.0, -1.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0]]  # invertible
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    D = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # no invertible

    matriz = matriz_en_main

    # Instanciamos objetos Java
    matriz_java = Matrix(matriz)
    servicio = MatrixService()

    print("--- Resultados desde el motor Java (vía JPype) ---")

    # Determinante
    det = servicio.calculateDeterminant(matriz_java)
    print(f"Determinante calculado: {det}")

    # Inversa
    if servicio.isInvertible(matriz_java):
        print("La matriz es invertible.")
        inversa_java = servicio.calculateInverse(matriz_java)

        print("Matriz Inversa recuperada:")
        # getData() nos devuelve el double[][] de Java
        for fila in inversa_java.getData():
            print([round(float(val), 3) for val in fila])
    else:
        print("La matriz no es invertible.")


if __name__ == "__main__":
    inicio = time.time()
    print("===" * 10)
    try:
        probar_motor_java()
    except Exception as e:
        print(f"Error en la conexión: {e}")
    finally:
        # Es buena práctica cerrar, aunque en scripts cortos no es crítico
        # jpype.shutdownJVM()
        pass
    fin = time.time()
    print(f"Tiempo total: {fin - inicio:.5f} segundos")
