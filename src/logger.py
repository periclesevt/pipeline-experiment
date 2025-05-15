import logging
from config import PATHS

# Configuração única de logger
def setup_logger():
    log_file = PATHS['logs']
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('pipeline')
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    )

    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger