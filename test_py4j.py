from py4j.java_gateway import JavaGateway, GatewayParameters
import time


def python_to_java_double_array(gateway, data):
    """
    Convierte una lista de listas de Python a un array double[][] nativo de Java.
    Necesario porque Py4J no mapea automáticamente listas a arrays primitivos.
    """
    filas = len(data)
    columnas = len(data[0])

    # Creamos el molde del array en la JVM (comunicación con servidor Java)
    java_array = gateway.new_array(gateway.jvm.double, filas, columnas)

    # Transferimos los datos
    for i in range(filas):
        for j in range(columnas):
            java_array[i][j] = float(data[i][j])

    return java_array


def ejecutar_prueba():
    # 1. Conexión al servidor Java (debe estar corriendo previamente)
    gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
    app = gateway.entry_point  # Acceso a la instancia de Main.java

    # 2. Definición de datos
    matriz_data = [[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]]

    try:
        # 3. Preparación de objetos Java
        # Convertimos los datos al formato que Java entiende
        java_array = python_to_java_double_array(gateway, matriz_data)

        # Obtenemos los servicios del motor
        servicio = app.getDetService()
        matriz_java = app.createMatrix(java_array)

        # 4. Cálculos
        print("--- Ejecutando motor Java vía Py4J ---")
        determinante = servicio.calculateDeterminant(matriz_java)
        print(f"Resultado del determinante: {determinante}")

        if servicio.isInvertible(matriz_java):
            inversa = servicio.calculateInverse(matriz_java)
            print("Matriz inversa calculada correctamente.")
            print("\nMatriz Inversa recuperada:")
            # getData() nos devuelve el double[][] de Java
            for fila in inversa.getData():
                print([round(float(val), 3) for val in fila])
        else:
            print("La matriz no es invertible.")

    except Exception as e:
        print(f"Error durante la ejecución: {e}")


if __name__ == "__main__":
    inicio = time.time()

    print("=" * 40)
    ejecutar_prueba()
    print("=" * 40)

    fin = time.time()
    print(f"Tiempo de ejecución: {fin - inicio:.5f} segundos")
