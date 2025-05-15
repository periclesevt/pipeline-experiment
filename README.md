# Pipeline de ETL de Vendas

Este repositório implementa um pipeline de ETL (Extract, Transform, Load) para dados de vendas, clientes e produtos. Ideal para portfólio de estágio, demonstra:

* Carregamento de múltiplos formatos (CSV, JSON)
* Tratamento de inconsistências (datas, tipos, valores nulos)
* Merge e filtragem de dados críticos
* Cálculo de indicadores (total de vendas, lucro)
* Geração de logs detalhados

---

## Estrutura de Pastas

```plaintext
data-pipeline/
├── data/
│   ├── input/            # Arquivos de entrada: vendas.csv, clientes.json, produtos.csv
│   ├── output/           # Saída gerada: vendas_processadas.csv
│   └── logs/             # Logs de execução: pipeline.log
├── src/                  # Código-fonte do pipeline
│   ├── __init__.py
│   ├── config.py         # Definições de caminhos e regras de validação
│   ├── logger.py         # Configuração de logging unificado
│   ├── loader.py         # Funções de leitura de dados
│   ├── transformer.py    # Limpeza e transformações (datas, merges)
│   ├── validator.py      # Verificações de colunas e valores
│   └── run_pipeline.py   # Script principal de execução
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação (este arquivo)
```

---

## Descrição do Fluxo

1. **Extract**

   * Lê `data/input/vendas.csv`, `clientes.json` e `produtos.csv`.

2. **Transform**

   * Formata e valida datas (descarta inválidas).
   * Converte e filtra `customer_id`, mantém apenas clientes `active`.
   * Normaliza nomes de produto, faz merge com `unit_cost`.
   * Calcula `total_sale` e `profit`.
   * Gera avisos de preços abaixo do mínimo.

3. **Load**

   * Escreve `data/output/vendas_processadas.csv`.
   * Registra logs em `data/logs/pipeline.log`.

---

## Detalhes de Input e Output

| Arquivo de Input | Formato | Descrição                                      |
| ---------------- | ------- | ---------------------------------------------- |
| `vendas.csv`     | CSV     | sale\_id, date, product, quantity, unit\_price |
| `clientes.json`  | JSON    | customer\_id, status, country                  |
| `produtos.csv`   | CSV     | product\_name, unit\_cost                      |

| Arquivo de Output        | Formato | Descrição                                                |
| ------------------------ | ------- | -------------------------------------------------------- |
| `vendas_processadas.csv` | CSV     | Vendas filtradas e enriquecidas com total\_sale e profit |
| `pipeline.log`           | TXT     | Logs de execução e erros/avisos                          |

---

## Como Executar

1. Clone o repositório:

   ```bash
   git clone <URL_DO_REPO>
   cd data-pipeline
   ```
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Coloque seus arquivos em `data/input/`:

   * `vendas.csv`, `clientes.json`, `produtos.csv` (Segue no projeto as pastas com amostras de dados gerados 
   aleatoriamente)
4. Execute:

   ```bash
   python -m src.run_pipeline
   ```
5. Verifique:

   * Resultado em `data/output/vendas_processadas.csv`
   * Logs em `data/logs/pipeline.log`

---

## Dependências

Conteúdo do `requirements.txt`:

```
pandas~=2.2.3
```
