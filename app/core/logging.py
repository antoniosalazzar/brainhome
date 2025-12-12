import logging
import logging.config
from pythonjsonlogger import jsonlogger


def setup_logging(level: str = "INFO"):

    fmt = '%(asctime)s - %(levelname)s - %(name)s  - %(message)s'

    # Logging global básico
    logging.basicConfig(
        level=level, 
        format=fmt,
    )

    # root logger
    logger = logging.getLogger()

    # # Handler para JSON (opcional)
    # logHandler = logging.StreamHandler()
    # formatter = jsonlogger.JsonFormatter(
    #     '%(asctime)s %(levelname)s %(name)s %(message)s'
    # )
    # logHandler.setFormatter(formatter)

    # # Añadir handler JSON al root logger
    # logger.addHandler(logHandler)
    # logger.setLevel(level)

    # Uvicorn logger
    uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access"]
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = logger.handlers
        uvicorn_logger.setLevel(level)

    return logger