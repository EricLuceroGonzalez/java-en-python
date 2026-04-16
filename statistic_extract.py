import re
import statistics
import matplotlib.pyplot as plt
import numpy as np


def analizar_log_secuencial(archivo):
    # Patrones para el formato de ejecución simple
    p_java = r"PROMEDIO JAVA: ([\d.]+) segundos"
    p_socket = r"PROMEDIO SOCKET: ([\d.]+) segundos"
    p_algoritmo = r"PROMEDIO ALGORITMO: ([\d.]+) segundos"
    p_total = r"TIEMPO TOTAL: ([\d.]+) segundos"

    java_times, socket_times, algo_times, total_times = [], [], [], []

    try:
        with open(archivo, "r") as f:
            contenido = f.read()
            java_times = [float(t) for t in re.findall(p_java, contenido)]
            algo_times = [float(t) for t in re.findall(p_algoritmo, contenido)]
            total_times = [float(t) for t in re.findall(p_total, contenido)]
            socket_times = [float(t) for t in re.findall(p_socket, contenido)]

        if total_times:
            print(f"📊 ANÁLISIS SECUENCIAL ({archivo})")
            print(f"Muestras: {len(algo_times)}")
            if socket_times != []:
                print(f"Promedio Socket:    {statistics.mean(socket_times):.8f} s")
            if java_times != []:
                print(f"Promedio Java:      {statistics.mean(java_times):.8f} s")
            print(f"Promedio Algoritmo: {statistics.mean(algo_times):.8f} s")
            print(f"Promedio Total:     {statistics.mean(total_times):.8f} s")
            print(f"Desviación Estndar: {statistics.stdev(total_times):.8f} s")
            print("-" * 40)
            return statistics.mean(total_times)
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")


def analizar_log_multihilo(archivo):
    # Patrón para el formato multi-hilo
    p_multi = r"Tiempo total para \d+ hilos: ([\d.]+) segundos"

    tiempos = []

    try:
        with open(archivo, "r") as f:
            contenido = f.read()
            tiempos = [float(t) for t in re.findall(p_multi, contenido)]

        if tiempos:
            print(f"🚀 ANÁLISIS MULTI-HILO ({archivo})")
            print(f"Ejecuciones: {len(tiempos)}")
            print(f"Tiempo Total Promedio: {statistics.mean(tiempos):.8f} s")
            print(f"Desviación Estándar:   {statistics.stdev(tiempos):.8f} s")
            print(f"Mejor Tiempo:          {min(tiempos):.8f} s")
            print("-" * 40)
            return statistics.mean(tiempos)
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")


def generar_grafico(data):
    labels = ["Secuencial", "Multi-hilo"]
    jpype_means = [data["jp_seq"], data["jp_multi"]]
    py4j_means = [data["py4j_seq"], data["py4j_multi"]]
    # jpype_means = [data["jp_seq_10x10"], data["jp_multi_10x10"]]
    # py4j_means = [data["py4j_seq_10x10"], data["py4j_multi_10x10"]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    barra1 = ax.bar(x - width / 2, jpype_means, width, label="JPype")
    barra2 = ax.bar(x + width / 2, py4j_means, width, label="Py4J")
    ax.bar_label(barra1, padding=3, fmt="%.5f s", fontsize=9, fontweight="bold")
    ax.bar_label(barra2, padding=3, fmt="%.5f s", fontsize=9, fontweight="bold")

    # Configuración
    ax.set_ylabel("Segundos (Escala Logarítmica)")
    ax.set_title("Comparativa de JPype vs Py4J en matriz 3x3")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, which="both", ls="-", alpha=0.2)

    plt.tight_layout()
    plt.savefig("comparativa_benchmarking_3x3.png")
    print("\nGráfico guardado como 'comparativa_benchmarking_3x3.png'")


if __name__ == "__main__":
    # Recolección de datos
    resultados = {
        "jp_seq": analizar_log_secuencial("log_ejecucion_jpype.log"),
        "py4j_seq": analizar_log_secuencial("log_ejecucion_py4j.log"),
        "jp_multi": analizar_log_multihilo("log_multihilo_jpype.log"),
        "py4j_multi": analizar_log_multihilo("log_multihilo_py4j.log"),
        # "jp_seq_10x10": analizar_log_secuencial("log_ejecucion_jpype_10x10.log"),
        # "py4j_seq_10x10": analizar_log_secuencial("log_ejecucion_py4j_10x10.log"),
        # "jp_multi_10x10": analizar_log_multihilo("log_multihilo_jpype_10x10.log"),
        # "py4j_multi_10x10": analizar_log_multihilo("log_multihilo_py4j_10x10.log"),
    }

    # Generar el gráfico si hay datos
    if any(resultados.values()):
        generar_grafico(resultados)
