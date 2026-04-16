import threading
import time
from py4j.java_gateway import JavaGateway, GatewayParameters
from tests_logger import setup_logging

# Inicializamos el log para Py4J
# setup_logging("log_multihilo_py4j.log")
setup_logging("log_multihilo_py4j_10x10.log")


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

        # --- Ejecución ---
        res = servicio.calculateDeterminant(m_java)
        # print(f"[Hilo {thread_id}] Determinante calculado: {res:.16f}")

    except Exception as e:
        print(f"[ERROR Hilo {thread_id}] {e}")
    finally:
        gateway.close()


def lanzar_test():
    data = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]
    C = [[1.0, -3.0, 2.0], [2.0, 5.0, 0.0], [0.0, -1.0, -2.0]]  # invertible
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
    print("===" * 12)
    print(f"Prueba con matriz 10x10, determinante e inversa con 5 hilos (PY4J)")
    hilos = []
    t_inicio_total = time.perf_counter()
    for i in range(5):
        t = threading.Thread(target=tarea_matriz_py4j, args=(i, matrix_test))
        hilos.append(t)
        t.start()
    for t in hilos:
        t.join()

    t_final_total = time.perf_counter()
    t_total = t_final_total - t_inicio_total
    print(f"Tiempo total para 5 hilos: {t_total:.6f} segundos")
    print("===" * 12)


if __name__ == "__main__":
    lanzar_test()
