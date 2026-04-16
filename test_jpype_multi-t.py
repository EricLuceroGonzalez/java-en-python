import threading
import jpype
import time
import os
from tests_logger import setup_logging

# setup_logging("log_multihilo_jpype.log")
setup_logging("log_multihilo_jpype_10x10.log")


def tarea_matriz_jpype(thread_id, matriz_data):
    # Acceso a la clase Thread de Java de forma moderna
    from jpype import java

    # Los hilos creados por Python (threading.Thread) son desconocidos para la JVM
    if not java.lang.Thread.isAttached():
        # Java no sabría dónde colocar las variables locales ni cómo gestionar el stack de ese hilo
        java.lang.Thread.attach()

    try:
        # Obtiene la clase de Java y crea la matriz.
        Main = jpype.JClass("matrixmath.Main")
        app_instance = Main()
        servicio = app_instance.getService()

        m_java = app_instance.createMatrix(matriz_data)

        # --- Ejecución ---
        res = servicio.calculateDeterminant(m_java)
        # print(f"[Hilo {thread_id}] Determinante calculado: {res:.16f}")
        if servicio.isInvertible(m_java):
            inv = servicio.calculateInverse(m_java)

    except Exception as e:
        print(f"[ERROR Hilo {thread_id}] {e}")


def lanzar_pruebas():
    jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jar_path])

    # Datos de prueba (Matriz C)
    A = [[1, 2], [1, 4]]  # invertible
    B = [[1.0, -1.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0]]  # invertible
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    D = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # no invertible
    matrix10 = [
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
    matrix_test = matrix10
    hilos = []

    print(
        f"--- Lanzando 5 hilos con JPype en matriz 10x10, (Python {pysys.version.split()[0]}) ---"
    )
    t_inicio_total = time.perf_counter()
    for i in range(5):
        # Creación de hilos independientes que ejecutan la misma tarea en JAVA con la misma matriz
        t = threading.Thread(target=tarea_matriz_jpype, args=(i, matrix_test))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    t_final_total = time.perf_counter()
    t_total = t_final_total - t_inicio_total
    print(f"Tiempo total para 5 hilos: {t_total:.6f} segundos")
    print("===" * 12)


if __name__ == "__main__":
    import sys as pysys

    lanzar_pruebas()
