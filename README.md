
# CalculadoraMatrices: Java-Python

Este proyecto implementa un motor de cálculo matricial desarrollado en Java, diseñado para ser consumido desde entornos Python. El sistema permite realizar operaciones utilizando dos arquitecturas de integración distintas: _JPype_ y _Py4J_.

> [!NOTE]  
> **Entorno de Desarrollo**: Este proyecto ha sido desarrollado en un entorno macOS.

---

## 📋 Tabla de Contenidos

* Requisitos del Sistema
* Arquitectura del Motor
* Compilación y Construcción
* Estrategias de Integración
* Análisis de Rendimiento (Benchmark)

---

## 💻 Requisitos del Sistema

* Sistema Operativo: macOS.
* Java SDK: 11 o superior.
* Apache Maven: Para la gestión de dependencias como Apache Commons Lang y POI.
* Python: 3.9+ gestionado con entorno virtual pipenv.

---

## 🏗️ Arquitectura del Motor

El núcleo lógico se organiza en el paquete `matrixmath`. La estructura comprende la entidad de datos, el servicio de cálculo y los puntos de entrada para los puentes de integración.

```mermaid
    classDiagram
        class Main {
            +main(args: String[])
            +getDetService() MatrixDet
            +createMatrix(data: double[][]) Matrix
        }

        class Matrix {
            -data: double[][]
            +Matrix(data: double[][])
            +getData() double[][]
            +print()
        }

        class MatrixDet {
            +calculateDeterminant(m: Matrix) double
            +calculateInverse(m: Matrix) Matrix
            +isInvertible(m: Matrix) boolean
        }

        Main ..> Matrix : "Instancia"
        Main ..> MatrixDet : "Instancia"
        MatrixDet ..> Matrix : "Procesa"
```

## Comandos rápidos

Para generar el JAR (_Java archive_), que se guarda en la carpeta ```/target```:

```bash
mvn clean package
```

Para probar que el motor Java funciona correctamente se ejecuta ese `.jar`:

```bash
java -cp target/calculadora-matrices-1.0-SNAPSHOT.jar math.Main
```

> [!WARNING]  
> Cada vez que se hacen cambios en java se debe actualizar todo el `/target` y el `.jar` ejecutando `mvn clean package`
>

## Notas de integración

Si uso JPype, tengo que pasarle la ruta del JAR al iniciar la JVM en el script de Python. Si al final decantamos por Py4J, se tiene que dejar el Main de Java ejecutando con el GatewayServer activo para que Python pueda conectar.

He configurado el ```pom.xml``` para que use Java 11, evitando problemas de compatibilidad con las librerías de Python. La carpeta ```/target``` está excluida en el `.gitignore` para no subir basura al repo, siguiendo la lógica del proyecto original.

## 🛠️ Compilación y Construcción

Para que el proyecto funcione con dependencias externas (como StringUtils), es crítico empaquetar el motor correctamente.

### Generación del Fat JAR

Para incluir todas las librerías dentro del archivo final, se utiliza el maven-shade-plugin:

``` bash
mvn clean package
```

### Gestión Dinámica de Dependencias

Si se prefiere cargar las librerías por separado desde Python, se deben copiar al directorio `/target`:

``` bash
mvn dependency:copy-dependencies
```

### Comando de empaquetado

Desde la raíz del proyecto (donde está el _pom.xml_), ejecuto:

```bash
mvn clean package
```

### ¿Cuándo tengo que ejecutar Maven?

1. **Primera ejecución:** Obligatorio para generar la carpeta ```/target``` y el JAR inicial.
2. **Cambios en el código:** Si modifico algo en ```Matrix.java``` o ```MatrixService.java```, tengo que volver a compilar. Si no lo hago, Python seguirá usando la lógica antigua guardada en el JAR.
3. **Limpieza:** Si borro la carpeta ```/target``` para liberar espacio, tendré que ejecutarlo de nuevo antes de volver a Python.


### Resultado del proceso

Si sale ```BUILD SUCCESS```, Maven crea el directorio ```/target``` y mete dentro el archivo ```calculadora-matrices-1.0-SNAPSHOT.jar```.
>Este es el archivo "motor" que se carga desde el script de Python.

Una vez ejecutado el comando `mvn clean package` crea dentro de `/target` las `/classes/`, es decir traduce `Main.java` a `Main.class` con cada archivo `.java`. La estructura de `/target` que queda luego de la primera ejecución de `mvn clean package` es:

```bash
    ├── calculadora-matrices-1.0-SNAPSHOT.jar
    ├── classes
    │   └── math
    │       ├── Main.class
    │       ├── Matrix.class
    │       └── MatrixService.class
    ├── generated-sources
    │   └── annotations
    ├── maven-archiver
    │   └── pom.properties
    └── maven-status
        └── maven-compiler-plugin
            └── compile
```

## 🔗 Estrategias de Integración

### JPype (Memoria Compartida)

JPype carga la JVM dentro del proceso de Python, permitiendo llamadas a nivel de memoria compartida. 

``` python
import jpype
import os

# Carga dinámica del classpath incluyendo dependencias externas
jar_path = "target/proyecto-abaco-0.0.1-SNAPSHOT.jar"
lib_folder = "target/dependency"
classpath = [jar_path]

if os.path.exists(lib_folder):
    for lib in os.listdir(lib_folder):
        if lib.endswith(".jar"):
            classpath.append(os.path.join(lib_folder, lib))

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=classpath)
```


```mermaid
      flowchart TB
 subgraph SG2["Máquina virtual Python"]
        B["Librería JPype1"]
        A["Script: test_jpype.py"]
  end
 subgraph SG3["JVM (Máquina Virtual Java)"]
        D["matrixmath.Matrix"]
        C{"Bridge JNI"}
        E["matrixmath.MatrixDet"]
  end
 subgraph SG1["Proceso unico (OS Process)"]
        SG2
        SG3
  end
    A --> B
    B <==> C
    C --> D & E

    style A fill:#4B8BBE,stroke:#333,color:#fff
    style C fill:#fff,stroke-dasharray: 5 5
    style D fill:#f89820,stroke:#333,color:#000
    style E fill:#f89820,stroke:#333,color:#000
    style SG1 fill:#b5fbff,stroke:#888,stroke-width:2px,color:#000
    style SG2 fill:#ffd43b,stroke:#888,stroke-width:2px,stroke-dasharray: 10 5,color:#000
    style SG3 fill:#A9BFEF, stroke:#888,stroke-width:2px,stroke-dasharray: 10 5,color:#000
```


1. __Preparación del motor Java:__ Es necesario compilar el proyecto con Maven para generar el artefacto en la carpeta target/:

```bash
mvn clean package
```

2. __Configuración del entorno Python:__ Instalar la dependencia mediante Pipenv:

```bash
pipenv install jpype1
```

3. __Código de integración:__ El script de Python debe apuntar al JAR generado en target/ antes de realizar los imports:

```python
    jar_path = os.path.join("target", "calculadora-matrices-1.0-SNAPSHOT.jar")
```

### Py4J (Arquitectura Cliente-Servidor)

Establece un puente mediante sockets TCP/IP. Requiere iniciar el GatewayServer desde Java antes de conectar desde Python.

``` bash
# Ejecución del servidor (Terminal 1)
mvn exec:java -Dexec.mainClass="matrixmath.Main"
```



```mermaid
    
    graph LR
    subgraph SG1 ["Maquina virtual Python"]
        A[Script: test_py4j.py] --> B[JavaGateway Client]
    end

    B <==>|TCP Socket Port: 25333| C[GatewayServer]

    subgraph SG2 ["Proceso Java (JVM)"]
        C --> D[Main.java]
        D --> E[matrixmath.Matrix]
        D --> F[matrixmath.MatrixDet]
    end

    style A fill:#4B8BBE,stroke:#333,color:#ffff
    style B fill:#444,stroke:#333,color:#ffff
    style D fill:#f89820,stroke:#333,color:#000
    style C fill:#444,color:#fff
    style E fill:#f89820,color:#000
    style F fill:#f89820,color:#000
    style SG1 fill:#ffd343,stroke:#888,stroke-width:2px,color:#000
    style SG2 fill:#A9BFEF,stroke:#888,stroke-width:2px,stroke-dasharray: 10 5,color:#000
```

1. __Dependencia en Java:__ 

    Añadir al archivo `pom.xml`. Este bloque le indica al gestor de dependencias que necesita la librería física de Py4J para poder compilar y ejecutarse.

    Sin esta línea, no se puede usar `import py4j.GatewayServer;` en Java, el compilador busca en sus archivos, no encuentra nada y lanza el error: `package py4j does not exist`.

    ```XML
    <dependency>
        <groupId>net.sf.py4j</groupId>
        <artifactId>py4j</artifactId>
        <version>0.10.9.7</version>
    </dependency>
    ```

2. __Servidor Java (Gateway):__ 
   
   Modificar el método main en `src/main/java/matrixmath/Main.java`:

    ```java
    public static void main(String[] args) {
        GatewayServer server = new GatewayServer(new Main());
        server.start();
        System.out.println("Servidor Py4J activo");
    }
    ```

3. __Código de integración en Python:__ 
    
    Instalar la librería:

    ```python
    pipenv install py4j
    ```

#### 1. Lanzamiento del Servidor Java (Terminal 1)

Antes de ejecutar el script de Python, el servidor Java debe estar "escuchando". Hay dos formas de lanzarlo:

- __Opción A__: Usando Maven (más fácil). _Maven se encarga de gestionar todas las librerías (incluida la de Py4J)_:

    ```Bash
    mvn exec:java -Dexec.mainClass="matrixmath.Main"
    ```

- __Opción B__: Usando el JAR directamente. _Incluir la librería de Py4J en el classpath manual_:

    ```Bash
    java -cp "target/calculadora-matrices-1.0-SNAPSHOT.jar:ruta/a/py4j.jar" matrixmath.Main
    ```

_(Nota: En Mac, el separador de carpetas es : y en Windows es ;)._

#### 2. Ejecución del Cliente Python (Terminal 2)

Una vez que en la Terminal 1 esté el Servidor Py4J activo, se lanza el __cliente Python__ con el script:

```Bash
pipenv run python test_py4j.py
```

Por ejemplo ejecutamos: 

```python
from py4j.java_gateway import JavaGateway

# Conexión al proceso Java externo
gateway = JavaGateway()
app = gateway.entry_point

# Acceso a los servicios definidos en el Main de Java
service = app.getDetService()
matriz = app.createMatrix([[1.0, 0.0], [0.0, 1.0]])

print(f"Resultado: {service.calculateDeterminant(matriz)}")
```

> [!WARNING]  
>**Diferencias en el manejo de tipos (Matrices 2D)**
>- **JPype**: Conversión transparente de `list[list]` a `double[][]`. Alta eficiencia.
>- **Py4J**: Requiere creación manual del array en la JVM mediante `gateway.new_array(gateway.jvm.double, rows, cols)`. Cada asignación de celda implica una comunicación por socket, lo que aumenta la latencia en matrices >grandes.
>

## 📊 Análisis de Rendimiento (Benchmark)

Resultados obtenidos tras promediar 10 ejecuciones de cálculo matricial 3x3.

>Calculo de:
>_Determinante -> Invertibilidad -> Inversa_

| Motor de Integración | Tiempo Promedio (s) |
| :--- | :--- | 
| JPype | 0.000647 |
| Py4J | 0.005136 | 

Conclusión Técnica: La penalización en Py4J se debe a la serialización de datos a través de sockets locales, mientras que JPype opera directamente en la memoria del proceso.

---

## 🚀 Flujo de Trabajo

Pasos para ejecutar el método `main` de una clase Java utilizando tanto __JPype__ como __Py4J__.

```mermaid
    flowchart TD
    %% Nodos de Inicio y Preparación Común (Java)
    Start([Inicio: Ejecutar Main en Java]) --> JavaSetup["Crear o Modificar Main.java<br/>Incluir lógica en 'public static void main'"]
    JavaSetup --> MavenBuild["Compilar y Empaquetar:<br/>Ejecutar 'mvn clean package'"]
    MavenBuild --> JarVerify{¿Se generó el JAR en target/?}
    JarVerify -- No --> MavenBuild
    JarVerify -- Sí --> ChooseLib

    %% Bifurcación de Decisión
    ChooseLib{¿Qué librería usar?}

    %% === Rama JPype ===
    ChooseLib -- JPype --> JPypeSetup["Python: Instalar jpype1<br/>'pipenv install jpype1'"]
    JPypeSetup --> JPypeStart["Python: Iniciar JVM<br/>'jpype.startJVM(classpath=[...])'"]
    JPypeStart --> JPypeImport["Python: Importar Clase<br/>'from paquete import Main'"]
    JPypeImport --> JPypeExec["Python: Llamar al método main<br/>'Main.main([])'"]
    JPypeExec --> JPypeStdout["El System.out de Java aparece<br/>en la terminal de Python"]
    JPypeStdout --> End

    %% === Rama Py4J ===
    ChooseLib -- Py4J --> Py4JSetup["Python: Instalar py4j<br/>'pipenv install py4j'"]
    Py4JSetup --> Terminal1[Abrir Terminal 1: Servidor]
    Terminal1 --> Py4JServerStart["Java: Iniciar GatewayServer<br/>mvn exec:java -Dexec.mainClass='...'"]
    Py4JServerStart --> Py4JWait["Esperar mensaje: 'Servidor activo'"]
    Py4JWait --> Terminal2[Abrir Terminal 2: Cliente]
    Terminal2 --> Py4JClientConnect["Python: Conectar al Gateway<br/>'gateway = JavaGateway()'"]
    Py4JClientConnect --> Py4JExec["Python: Llamar al main (si está expuesto)<br/>'gateway.entry_point.main([])'"]
    Py4JExec --> Py4JStdout["El System.out de Java aparece<br/>en la Terminal 1 (Servidor)"]
    Py4JStdout --> End

    %% Nodos de Fin
    End([Fin: Main Ejecutado])

    %% Estilos
    style Terminal1 fill:#a4fcc6,stroke:#333,stroke-width:2px,color:#000
    style Terminal2 fill:#a4fcc6,stroke:#333,stroke-width:2px,color:#000
    style ChooseLib fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    style MavenBuild fill:#ff9,stroke:#333,stroke-width:2px,color:#000
    style JPypeSetup fill:#ffd343,stroke:#333,color:#000
    style JPypeStart fill:#ffd343,stroke:#333,color:#000
    style JPypeImport fill:#ffd343,stroke:#333,color:#000
    style JPypeExec fill:#ffd343,stroke:#333,color:#000,stroke-width:2px
    style Py4JSetup fill:#ffd343,stroke:#333,color:#000,stroke-width:2px
    style Py4JClientConnect fill:#ffd343,stroke:#333,color:#000,stroke-width:2px
    style Py4JExec fill:#ffd343,stroke:#333,color:#000,stroke-width:2px
    style Py4JServerStart fill:#fcf,stroke:#333,stroke-width:2px
```