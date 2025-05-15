import argparse
from config import PATHS, VALIDATION_RULES
from logger import setup_logger
from loader import load_data
from transformer import formatar_datas, filtrar_clientes_ativos, calcular_totais
from validator import validar_dados


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline de ETL de vendas"
    )
    parser.add_argument(
        '--paths', help='Caminhos de configuração', action='store_true'
    )
    args = parser.parse_args()

    logger = setup_logger()
    try:
        # 1. Carregamento
        vendas = load_data(PATHS['input_vendas'])
        clientes = load_data(PATHS['input_clientes'])
        produtos = load_data(PATHS['input_produtos'])

        # 2. Transformações
        vendas = formatar_datas(vendas)
        vendas = filtrar_clientes_ativos(vendas, clientes)
        vendas = calcular_totais(vendas, produtos, VALIDATION_RULES['valor_minimo'])

        # 3. Validação
        erros = validar_dados(vendas, VALIDATION_RULES['colunas_obrigatorias'])
        if erros:
            logger.error("Terminado com erros de validação.")
            return

        # 4. Salvamento
        PATHS['output'].parent.mkdir(parents=True, exist_ok=True)
        vendas.to_csv(PATHS['output'], index=False)
        logger.info(f"Pipeline concluído: {PATHS['output']}")

    except Exception as e:
        logger.exception(f"Pipeline falhou: {e}")


if __name__ == '__main__':
    main()