import threading
import jpype
import time
import os
from tests_logger import setup_logging

setup_logging("log_multihilo_jpype.log")


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

        inicio_real = time.perf_counter()
        inicio_cpu = time.process_time()

        # --- Ejecución ---
        res = servicio.calculateDeterminant(m_java)

        fin_real = time.perf_counter()
        fin_cpu = time.process_time()

        t_real = fin_real - inicio_real
        t_cpu = fin_cpu - inicio_cpu

        print(
            f"[Hilo {thread_id}] |Det: {res:.2f} |  Real: {t_real:.6f} s | CPU: {t_cpu:.6f} s"
        )

    except Exception as e:
        print(f"[ERROR Hilo {thread_id}] {e}")


def lanzar_pruebas():
    jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jar_path])

    data = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]
    hilos = []

    print(
        f"--- Lanzando 5 hilos con JPype en matriz C, (Python {pysys.version.split()[0]}) ---"
    )
    for i in range(5):
        # Creación de hilos independientes que ejecutan la misma tarea en JAVA con la misma matriz
        t = threading.Thread(target=tarea_matriz_jpype, args=(i, data))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()


if __name__ == "__main__":
    import sys as pysys

    lanzar_pruebas()
