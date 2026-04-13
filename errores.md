## Errores al ejecutar mvn:
```bash
[INFO] Scanning for projects...
[ERROR] [ERROR] Some problems were encountered while processing the POMs:
[FATAL] Non-parseable POM /Users/ericlucero/Documents/Academic/Python_Fun/Random_projcts/Java/CalculadoraMatrices/pom.xml: expected > to end empty tag not 4 (position: TEXT seen ... http://maven.apache.org/xsd/maven-4.0.0.xsd">\n    <modelVersion/4... @4:20)  @ line 4, column 20
 @ 
[ERROR] The build could not read 1 project -> [Help 1]
[ERROR]   
[ERROR]   The project  (/Users/ericlucero/Documents/Academic/Python_Fun/Random_projcts/Java/CalculadoraMatrices/pom.xml) has 1 error
[ERROR]     Non-parseable POM /Users/ericlucero/Documents/Academic/Python_Fun/Random_projcts/Java/CalculadoraMatrices/pom.xml: expected > to end empty tag not 4 (position: TEXT seen ... http://maven.apache.org/xsd/maven-4.0.0.xsd">\n    <modelVersion/4... @4:20)  @ line 4, column 20 -> [Help 2]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/ProjectBuildingException
[ERROR] [Help 2] http://cwiki.apache.org/confluence/display/MAVEN/ModelParseException
```

### Solucion: 
Hubo un error de escritura en el `pom.xml`

## Error al instalar jpype1 usando el entorno pipenv
Si el error es _CMake no encuentra el JNI (Java Native Interface)_, jpype necesita encontrar el JAVA instalado localmente en Mac.

### Soluciones

1. Definir el JAVA_HOME correctamente

CMake necesita que la variable `JAVA_HOME` apunte al directorio raíz de tu JDK para localizar los componentes que le faltan (`JAVA_INCLUDE_PATH` y `JAVA_INCLUDE_PATH2`).

Ejecutar en terminal (esto configurará la ruta para la sesión actual):

```bash
export JAVA_HOME=$(/usr/libexec/java_home)
export PATH=$JAVA_HOME/bin:$PATH
```

2. Instalar dependencias de compilación
Si el error menciona problemas con `ninja`, asegúrate de tener las herramientas necesarias instaladas vía Homebrew:

```bash
brew install cmake ninja
```

3. Forzar instalacion en Pipenv
Ahora con las variables de entorno listas, se vuelve a intentar la instalación. Se hace dentro de la carpeta del proyecto:

```bash
pipenv install jpype1
```
