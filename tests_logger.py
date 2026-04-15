import logging
import sys
import os


def setup_logging(log_name="test_java-python.log"):
    # Configuración básica del logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_name, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Clase para redirigir print() y salidas de Java al logger
    class LoggerWriter:
        def __init__(self, level):
            self.level = level

        def write(self, message):
            if message.strip():
                self.level(message.strip())

        def flush(self):
            pass

    # Redirección de la salida estándar y de errores
    sys.stdout = LoggerWriter(logging.info)
    sys.stderr = LoggerWriter(logging.error)

    return logging.getLogger()
