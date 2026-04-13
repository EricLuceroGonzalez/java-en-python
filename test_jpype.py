import jpype
import jpype.imports
from jpype.types import *
import os

# 1. Configuración de rutas
jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")

# 2. Inicio de la JVM
if not jpype.isJVMStarted():
    # El classpath apunta al JAR que compilamos con Maven
    jpype.startJVM(classpath=[jar_path])

# 3. Import de clases Java (ahora que la JVM está arriba)
from math import Matrix, MatrixService


def probar_motor_java():
    # Definimos una matriz 3x3 que sabemos que tiene inversa
    # A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    datos = [[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]]

    # Instanciamos objetos Java
    m = Matrix(datos)
    servicio = MatrixService()

    print("--- Resultados desde el motor Java (vía JPype) ---")

    # Determinante
    det = servicio.calculateDeterminant(m)
    print(f"Determinante calculado: {det}")

    # Inversa
    if servicio.isInvertible(m):
        print("La matriz es invertible.")
        inversa_java = servicio.calculateInverse(m)

        print("Matriz Inversa recuperada:")
        # getData() nos devuelve el double[][] de Java
        for fila in inversa_java.getData():
            print([round(float(val), 3) for val in fila])
    else:
        print("La matriz no es invertible.")


if __name__ == "__main__":
    try:
        probar_motor_java()
    except Exception as e:
        print(f"Error en la conexión: {e}")
    finally:
        # Es buena práctica cerrar, aunque en scripts cortos no es crítico
        # jpype.shutdownJVM()
        pass
