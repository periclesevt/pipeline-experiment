from pathlib import Path
from typing import List, Dict

# Caminhos de entrada/saída e regras de validação
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

PATHS: Dict[str, Path] = {
    'input_vendas': DATA_DIR / 'input' / 'vendas.csv',
    'input_clientes': DATA_DIR / 'input' / 'clientes.json',
    'input_produtos': DATA_DIR / 'input' / 'produtos.csv',
    'output': DATA_DIR / 'output' / 'vendas_processadas.csv',
    'logs': DATA_DIR / 'logs' / 'pipeline.log',
}

VALIDATION_RULES: Dict[str, object] = {
    'colunas_obrigatorias': ['sale_id', 'date', 'product', 'customer_id'],
    'valor_minimo': 0.01,
}