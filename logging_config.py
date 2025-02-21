import logging
import os

def setup_logging():
    # Obtener la ruta absoluta del directorio principal del proyecto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log_directory = os.path.join(base_dir, "logs")
    os.makedirs(log_directory, exist_ok=True)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                        handlers=[logging.FileHandler(os.path.join(log_directory, "prueba.rtf")),
                                  logging.StreamHandler()])

    logger = logging.getLogger(__name__)

    return logger
