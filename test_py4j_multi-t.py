import threading
import time
from py4j.java_gateway import JavaGateway, GatewayParameters
from tests_logger import setup_logging

# Inicializamos el log para Py4J
setup_logging("log_multihilo_py4j.log")


def tarea_matriz_py4j(thread_id, matriz_data):
    # Iniciamos gateway para este hilo
    gateway = JavaGateway()
    try:
        app = gateway.entry_point

        # Java espera double[][], así que construimos el objeto nativo
        filas = len(matriz_data)
        columnas = len(matriz_data[0])

        # Creamos el array en la JVM
        java_array = gateway.new_array(gateway.jvm.double, filas, columnas)

        # Llenamos el array (Py4J se encarga de la conversión de float a double)
        for i in range(filas):
            for j in range(columnas):
                java_array[i][j] = float(matriz_data[i][j])

        # llamamos a createMatrix con el array correcto
        m_java = app.createMatrix(java_array)
        servicio = app.getService()

        inicio_real = time.perf_counter()
        inicio_cpu = time.process_time()

        # --- Ejecución ---
        res = servicio.calculateDeterminant(m_java)

        fin_real = time.perf_counter()
        fin_cpu = time.process_time()  # Python no puede medir el CPU de la JVM

        t_real = fin_real - inicio_real
        t_cpu = fin_cpu - inicio_cpu

        print(
            f"[Hilo {thread_id}] |Det: {res:.2f} |  Real: {t_real:.6f} s | CPU: {t_cpu:.6f} s"
        )

    except Exception as e:
        print(f"[ERROR Hilo {thread_id}] {e}")
    finally:
        gateway.close()


def lanzar_test():
    data = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
    print("===" * 12)
    print(f"Prueba con matriz C, determinante e inversa con 5 hilos (PY4J)")
    hilos = []
    for i in range(5):
        t = threading.Thread(target=tarea_matriz_py4j, args=(i, data))
        hilos.append(t)
        t.start()
    for t in hilos:
        t.join()


if __name__ == "__main__":
    lanzar_test()
