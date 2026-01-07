# Projeto N6 — Pipeline de Dados Analítico (Olist)

## Visão Geral

Este projeto implementa um **pipeline de dados analítico completo**, inspirado em um cenário real de e-commerce (Olist), com foco em **qualidade de dados, confiabilidade e boas práticas de Engenharia de Dados**.

O pipeline transforma dados brutos (CSV) em dados **padronizados, validados e prontos para análise**, utilizando arquitetura em camadas (Bronze → Silver → Gold), testes automatizados e controle explícito de erros e rejeições.

O objetivo principal é evoluir a maturidade técnica do pipeline para um **nível profissional**, próximo ao que é utilizado em ambientes corporativos.

---

## Objetivos do Projeto

- Construir um pipeline de dados organizado e escalável  
- Aplicar boas práticas de Engenharia de Dados  
- Garantir qualidade e integridade dos dados  
- Separar claramente:
  - erros fatais
  - registros rejeitados (rejects)
- Preparar dados confiáveis para análises e dashboards (Power BI / SQL)

---

## Arquitetura do Pipeline

Bronze (dados brutos)
↓
Silver (dados limpos, validados e padronizados)
↓
Gold (camada analítica e métricas)

markdown
Copiar código

### Bronze
- Dados brutos em CSV
- Organização por `ingest_date`
- Nenhuma regra de negócio aplicada

### Silver
- Limpeza e padronização
- Validação de regras de negócio
- Validação de PK e FK
- Separação entre dados válidos e rejeitados
- Geração de métricas de qualidade
- Testes automatizados

### Gold (planejado)
- Modelagem estrela
- KPIs e métricas analíticas
- Preparação para consumo por BI

---

## Tabela Fato e Granularidade

### Tabela Fato Principal
`olist_order_items_dataset`

### Granularidade
> **1 linha representa 1 item vendido em um pedido**

Essa granularidade permite análises detalhadas de:
- receita
- volume de vendas
- produtos
- vendedores
- comportamento temporal

A tabela `order_items` representa o menor nível de evento de venda, sendo a base correta para análises financeiras e operacionais.

---

## Chaves e Integridade dos Dados

### Chave Primária (PK)
- `(order_id, order_item_id)`

### Regras de PK
- Não pode ser nula
- Não pode ser duplicada

### Regras Gerais de Integridade
- IDs obrigatórios não podem ser nulos
- Valores monetários devem ser positivos
- Relações entre tabelas devem ser válidas

---

## Rejects vs Errors

### Rejects
Registros que violam regras de negócio, mas **não impedem a execução do pipeline**.

Exemplos:
- preço ≤ 0
- dados inconsistentes
- campos obrigatórios ausentes em uma linha específica

➡️ O pipeline continua  
➡️ Os registros são isolados para auditoria  

### Errors (Fatais)
Erros que comprometem a confiabilidade do dataset.

Exemplos:
- arquivo Bronze inexistente
- PK duplicada
- Silver vazia
- schema inválido

➡️ O pipeline é interrompido imediatamente

---

## Testes Automatizados

O projeto utiliza **pytest** para validar a qualidade da camada Silver.

### Tipos de Testes Implementados

- **Schema**
  - colunas obrigatórias
  - tipos esperados
- **Chave Primária**
  - não nula
  - não duplicada
- **Regras de Negócio**
  - `price > 0`
  - `freight_value ≥ 0`
- **Sanity Checks**
  - Silver não vazia
  - volumes coerentes

Os testes utilizam **fixtures isoladas**, garantindo confiabilidade e execução rápida.

---

## Estrutura do Projeto

projeto_n6/
│
├── data/
│ ├── bronze/
│ ├── silver/
│ ├── gold/
│ └── metrics/
│
├── logs/
│
├── src/projeto_n6/
│ ├── pipeline.py
│ ├── run_context.py
│ ├── paths.py
│ ├── settings.py
│ └── silver/
│ └── orders.py
│
├── tests/
│ └── silver/
│ ├── conftest.py
│ ├── test_orders_schema.py
│ ├── test_orders_pk.py
│ ├── test_orders_business_rules.py
│ └── test_orders_sanity.py
│
├── pyproject.toml
├── poetry.lock
└── README.md

yaml
Copiar código

---

## Tecnologias Utilizadas

- Python 3.13
- Pandas
- Pytest
- Poetry
- SQL
- Power BI (camada analítica futura)

---

## Como Executar o Projeto

### Instalar dependências
```bash
poetry install
Executar o pipeline
bash
Copiar código
poetry run python -m projeto_n6.pipeline
Executar os testes
bash
Copiar código
poetry run pytest -v