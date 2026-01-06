# Gold Blueprint — Olist (Power BI) — Vendas + SLA (Nível 6)

## 1) Objetivo do produto (Dashboard)
Construir um dashboard executivo de **Vendas (A)** com um bloco de **SLA/Entrega (B)**, garantindo dados confiáveis via Silver e rastreabilidade via métricas do pipeline.

### Perguntas de negócio (KPIs)
**Vendas**
- Receita total
- Ticket médio (AOV)
- Itens mais comprados (volume)
- Categorias mais vendidas (volume/receita)
- Região (UF/Cidade) com maior receita e maior volume
- Sazonalidade: meses/dias com pico e queda

**Entrega / SLA**
- Tempo compra → entrega (dias)
- % entregas atrasadas (entregue após data estimada)
- Estados / vendedores com mais atraso

**Qualidade / Satisfação**
- Nota média de review
- Distribuição de reviews (1 a 5)
- Relação atraso x review (comparação simples)

---

## 2) Tabela Fato Principal (Gold)
A fato principal para análises de vendas será baseada em `order_items` (granularidade mais fina).

### fact_sales_item (principal)
**Granularidade**
- 1 linha = 1 item vendido em um pedido (order_id + order_item_id)

**Chaves**
- PK: (order_id, order_item_id)
- FKs:
  - order_id → dim_orders
  - product_id → dim_products
  - seller_id → dim_sellers
  - customer_id (via orders) → dim_customers
  - date_key → dim_date

**Campos principais**
- price
- freight_value
- (opcional) revenue_item = price + freight_value (decisão de negócio: confirmar definição de receita)

---

## 3) Outras Tabelas Fato (Gold) — opcionais/apoio
### fact_payments
- 1 linha = 1 pagamento
- Uso: receita confirmada por pagamento, tipos de pagamento, parcelamento

### fact_reviews
- 1 linha = 1 review (por pedido)
- Uso: satisfação, score, correlação simples com atraso

### fact_orders (ou dim_orders dependendo do modelo)
- 1 linha = 1 pedido
- Uso: status do pedido, datas do ciclo, SLA de entrega (base principal)

---

## 4) Dimensões (Gold)
### dim_date
- dia, mês, ano, trimestre, nome do mês, etc.
- usada para sazonalidade e séries temporais

### dim_customers
- customer_unique_id, cidade, estado, CEP (conforme qualidade)
- usada para análises regionais (lado do cliente)

### dim_sellers
- cidade, estado
- usada para análises regionais (lado do vendedor)

### dim_products
- categoria, atributos do produto (peso, dimensões, fotos)
- inclui categoria traduzida quando aplicável

### dim_orders (dimensão de processo)
- order_status
- timestamps do ciclo do pedido
- cálculo de SLA (compra→entrega, atraso vs estimativa)

---

## 5) Métricas alvo (Power BI) — definição conceitual
### Vendas
- Receita Total: soma de valores de venda (definir se via payments ou via items)
- Ticket Médio (AOV): Receita Total / Nº de pedidos
- Itens mais comprados: TOP produtos por quantidade de itens
- Top categorias: por receita e por volume
- Região campeã: UF/cidade com maior receita/volume
- Picos e quedas: receita por mês (e comparação MoM)

### SLA / Entrega
- Lead time entrega (dias): delivered_customer_date - purchase_timestamp
- % Atraso: delivered_customer_date > estimated_delivery_date
- Atraso por UF / seller

### Reviews
- Nota média
- Distribuição 1..5
- Comparativo: atrasado vs não atrasado (review médio)

---

## 6) Requisitos que a Silver precisa garantir (contrato)
Para que a Gold funcione corretamente, a Silver deve garantir:

### Tipos corretos
- Datas como datetime (purchase, delivered, estimated, etc.)
- Valores monetários como numérico
- IDs como string (evitar perda por conversão)

### Integridade relacional
- order_items.order_id existe em orders
- order_items.product_id existe em products
- order_items.seller_id existe em sellers
- orders.customer_id existe em customers

### Regras de sanidade
- price > 0 (ou >= 0 conforme decisão)
- freight_value >= 0
- datas coerentes (purchase <= delivered quando delivered existe)
- status dentro do conjunto esperado

### Monitoramento
- registrar linhas de entrada/saída Bronze→Silver
- registrar duplicidades de PK e FKs órfãs
- registrar % de descarte e motivo

---

## 7) Decisões em aberto (para documentar)
1) Receita oficial será baseada em:
   - (A) `payments.payment_value` (mais “financeiro”) ou
   - (B) `order_items.price` (+ freight?) (mais “comercial”)
2) Geolocalização:
   - usar apenas UF/cidade do customers e sellers (mais simples)
   - ou enriquecer com geolocation (mais avançado)

---

## 8) Entregáveis finais
- Pipeline Bronze→Silver→Gold
- Tabelas Gold prontas para BI
- Dashboard Power BI (Vendas + SLA + Qualidade do Pipeline)
- Documentação (README + dicionário de dados + blueprints)
- Métricas de execução do pipeline (monitoramento)
