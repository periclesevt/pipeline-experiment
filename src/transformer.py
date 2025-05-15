import pandas as pd
from logger import setup_logger

logger = setup_logger()

def formatar_datas(df: pd.DataFrame, col: str = 'date') -> pd.DataFrame:
    # Se contiver barras, assumimos DD/MM/YYYY
    mask = df[col].str.contains('/', na=False)
    df.loc[mask, col] = pd.to_datetime(df.loc[mask, col], dayfirst=True, errors='coerce')
    df.loc[~mask, col] = pd.to_datetime(df.loc[~mask, col], errors='coerce')
    antes = len(df)
    df = df.dropna(subset=[col])
    logger.info(f"Datas formatadas. Registros descartados: {antes - len(df)}")
    return df

def filtrar_clientes_ativos(df_vendas: pd.DataFrame, df_clientes: pd.DataFrame) -> pd.DataFrame:
    """Descarta vendas com customer_id inválido, faz merge com clientes e retorna apenas ativos."""
    # 1) Harmoniza tipo de customer_id em vendas
    df_vendas['customer_id'] = pd.to_numeric(df_vendas['customer_id'], errors='coerce')
    antes = len(df_vendas)
    df_vendas = df_vendas.dropna(subset=['customer_id'])
    logger.info(f"IDs de cliente não numéricos descartados: {antes - len(df_vendas)}")

    # 2) Preenche países ausentes
    df_clientes = df_clientes.assign(country=df_clientes.get('country').fillna('--'))

    # 3) Garante tipo inteiro para merge
    df_clientes = df_clientes.astype({'customer_id': 'Int64'})

    # 4) Merge e filtragem de status
    merged = df_vendas.merge(
        df_clientes[['customer_id', 'status', 'country']],
        on='customer_id',
        how='left'
    )
    merged['status'] = merged['status'].fillna('unknown')

    ativo = merged[merged['status'] == 'active']
    logger.info(f"Clientes ativos mantidos: {ativo['customer_id'].nunique()}")
    return ativo

def calcular_totais(
    df_vendas: pd.DataFrame,
    df_produtos: pd.DataFrame,
    valor_minimo: float
) -> pd.DataFrame:
    """Une vendas a produtos, calcula total_sale e profit, e avisa sobre preços abaixo do mínimo."""
    # Normaliza nomes de produto
    df_vendas['product'] = df_vendas['product'].astype(str).str.strip().str.lower()
    df_produtos['product_name'] = df_produtos['product_name'].astype(str).str.strip().str.lower()

    merged = df_vendas.merge(
        df_produtos[['product_name', 'unit_cost']],
        left_on='product',
        right_on='product_name',
        how='left'
    )
    merged['unit_cost'] = merged['unit_cost'].fillna(0)
    merged['unit_price'] = merged['unit_price'].fillna(0)

    merged['total_sale'] = merged['quantity'] * merged['unit_price']
    merged['profit'] = merged['total_sale'] - (merged['quantity'] * merged['unit_cost'])

    # Log de vendas abaixo do valor mínimo
    below_min = merged[merged['unit_price'] < valor_minimo]
    if not below_min.empty:
        logger.warning(f"{len(below_min)} vendas abaixo do valor mínimo ({valor_minimo}).")

    return merged.drop(columns=['product_name'])

def validar_dados(
    df: pd.DataFrame,
    colunas_obrigatorias: list[str]
) -> list[str]:
    """Verifica se colunas obrigatórias existem e se não têm valores nulos."""
    erros: list[str] = []
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
