import pandas as pd
from pathlib import Path
from logger import setup_logger

logger = setup_logger()

def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        logger.error(f"Arquivo não encontrado: {path}")
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    suffix = path.suffix.lower()
    try:
        if suffix == '.csv':
            df = pd.read_csv(path)
        elif suffix in ['.json', '.geojson']:
            df = pd.read_json(path)
        else:
            raise ValueError(f"Formato não suportado: {suffix}")
        logger.info(f"Dados carregados com sucesso: {path.name}")
        return df
    except Exception as e:
        logger.exception(f"Falha ao carregar {path}: {e}")
        raise