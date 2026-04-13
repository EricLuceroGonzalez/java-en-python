# CalculadoraMatrices

Librería sencilla en Java para sacar determinantes e inversas (2x2 y 3x3). La idea es compilar esto como un **JAR** y usarlo de motor de cálculo en Python, aprovechando una estructura ya existente en Java.

## Estructura de este proyecto

- math.Matrix: El objeto matriz básico.
- math.MatrixService: Los cálculos (determinante, inversa, etc.).
- math.Main: Para probar que todo rula desde la consola.

## Comandos rápidos

Para generar el JAR (se guarda en la carpeta ```/target```):

```bash
mvn clean package
```

Para probar que el motor Java funciona correctamente:

```bash
java -cp target/calculadora-matrices-1.0-SNAPSHOT.jar math.Main
```

## Notas de integración

Si uso JPype, tengo que pasarle la ruta del JAR al iniciar la JVM en el script de Python. Si al final decantamos por Py4J, se tiene que dejar el Main de Java corriendo con el GatewayServer activo para que Python pueda conectar.

He configurado el ```pom.xml``` para que use Java 11, evitando problemas de compatibilidad con las librerías de Python. La carpeta ```/target``` está excluida en el `.gitignore` para no subir basura al repo, siguiendo la lógica del proyecto original.