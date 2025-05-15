from typing import List
from logger import setup_logger
import pandas as pd

logger = setup_logger()

def validar_dados(
    df: 'pd.DataFrame',
    colunas_obrigatorias: List[str]
) -> List[str]:
    """Verifica se colunas obrigatórias existem e sem valores nulos."""
    erros = []
    for col in colunas_obrigatorias:
        if col not in df.columns:
            erros.append(f"Coluna obrigatória ausente: {col}")
        elif df[col].isna().any():
            erros.append(f"Valores ausentes na coluna: {col}")

    if erros:
        for e in erros:
            logger.error(e)
    else:
        logger.info("Validação de colunas concluída sem erros.")

    return erros