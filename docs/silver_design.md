# Silver Layer Design — Projeto Olist (Nível 6)

## 1. Objetivo da Camada Silver

A camada **Silver** tem como objetivo transformar os dados brutos (Bronze) em dados **confiáveis, padronizados e validados**, prontos para modelagem analítica na camada Gold.

Nesta camada são aplicadas:
- limpeza de dados
- normalização
- padronização
- correções de tipos
- validações de qualidade
- checagens de integridade relacional

A Silver **não cria métricas analíticas finais** nem agregações para BI.

---

## 2. Tabela Fato Principal

### 2.1 Identificação da Tabela Fato

A tabela fato principal do projeto é:

**`olist_order_items_dataset`**

### 2.2 Granularidade

A granularidade da tabela fato é definida como:

> **1 linha representa 1 item vendido em um pedido.**

Essa granularidade permite análises detalhadas de:
- receita
- volume de vendas
- frete
- produto
- vendedor
- comportamento ao longo do tempo

### 2.3 Justificativa

Apesar de existirem outras tabelas transacionais (orders, payments, reviews), a tabela `order_items` representa o **menor nível de evento de venda**, sendo a base correta para análises financeiras e operacionais.

---

## 3. Tabelas de Dimensão

As tabelas de dimensão fornecem **contexto descritivo** para a tabela fato, sem conter métricas numéricas principais.

Dimensões do projeto:

- **`olist_customers_dataset`** → informações do cliente
- **`olist_products_dataset`** → informações do produto
- **`olist_sellers_dataset`** → informações do vendedor
- **`olist_orders_dataset`** → datas e status do pedido
- **`olist_order_payments_dataset`** → forma e valores de pagamento
- **`olist_order_reviews_dataset`** → avaliações dos clientes
- **`olist_geolocation_dataset`** → localização geográfica
- **`product_category_name_translation`** → tradução das categorias de produto

Essas dimensões serão utilizadas na **modelagem estrela** na camada Gold.

---

## 4. Responsabilidades da Camada Silver

A camada Silver é responsável por:

- limpeza de dados inconsistentes
- normalização de textos (acentos, caixa, espaços)
- padronização de formatos (datas, números, códigos)
- conversão correta de tipos de dados
- validação de chaves primárias (PK)
- validação de chaves estrangeiras (FK)
- aplicação de regras de qualidade de dados
- execução de sanity checks

A camada Silver **não deve**:
- criar métricas finais
- realizar agregações analíticas
- preparar dados diretamente para visualização em BI

---

## 5. Regras de Qualidade de Dados

### 5.1 Regras Gerais

- Chaves primárias não podem ser nulas
- Chaves primárias não podem conter duplicidades
- Chaves estrangeiras devem existir na tabela de referência
- Valores monetários devem ser positivos
- Datas inválidas ou fora do intervalo esperado devem ser tratadas
- Campos obrigatórios não podem ser nulos

### 5.2 Exemplos de Regras por Tabela

**`olist_order_items_dataset`**
- `order_id` não pode ser nulo
- `product_id` deve existir em `products`
- `seller_id` deve existir em `sellers`
- `price` > 0
- `freight_value` ≥ 0

**`olist_customers_dataset`**
- `customer_id` não pode ser nulo
- `customer_state` deve ser um estado válido
- `customer_zip_code_prefix` deve ser numérico

---

## 6. Uso de Ferramentas na Camada Silver

### 6.1 Python

Python será utilizado para:
- limpeza textual (acentos, maiúsculas/minúsculas)
- normalização de strings
- tratamento de datas inválidas
- conversão de tipos
- regras de validação linha a linha
- enriquecimento leve de dados

### 6.2 SQL

SQL será utilizado para:
- validação de chaves primárias (PK)
- validação de chaves estrangeiras (FK)
- detecção de duplicidades
- contagem de registros entre camadas
- sanity checks relacionais

## Validação de Chaves

A camada Silver valida a integridade dos dados através de:

- verificação de unicidade e não nulidade das chaves primárias
- validação da existência das chaves estrangeiras nas tabelas de referência
- identificação de registros órfãos
- comparação de volumes entre camadas

Essas validações garantem a consistência relacional antes da modelagem analítica.

---

## 7. Sanity Checks

Sanity checks são verificações simples para garantir que os dados fazem sentido, como:
- ausência de valores monetários negativos
- datas no intervalo esperado
- volumes de dados compatíveis entre Bronze e Silver
- integridade entre tabelas relacionadas

Essas verificações ajudam a detectar erros rapidamente antes da camada Gold.

---

## 8. Resultado Esperado da Silver

Ao final da camada Silver, os dados devem estar:
- limpos
- padronizados
- validados
- confiáveis
- prontos para modelagem analítica na camada Gold

A Silver estabelece a **base de confiança** do pipeline de dados.
