# 🥇 Gold Blueprint — Olist  
## Dashboard Power BI | Vendas + SLA

---

## 1. Objetivo
Construir um dashboard executivo com foco em:
- **Vendas**
- **Entrega / SLA**
- **Qualidade (Reviews)**

Os dados são consolidados na **camada Gold**, a partir da Silver, garantindo consistência analítica e rastreabilidade.

---

## 2. Perguntas de Negócio (KPIs)

### Vendas
- Receita total
- Ticket médio (AOV)
- Produtos e categorias mais vendidos
- Regiões (UF / Cidade) com maior performance
- Sazonalidade (mês e dia)

### SLA / Entrega
- Tempo médio de entrega (dias)
- % de pedidos atrasados
- Atraso por estado e vendedor

### Qualidade
- Nota média de review
- Distribuição de notas (1 a 5)
- Comparação: atrasado × não atrasado

---

## 3. Modelagem Gold

### Fato Principal
#### `fact_sales_item`
- **Granularidade**: 1 item por pedido  
- **PK**: (order_id, order_item_id)
- **Métricas**:
  - price
  - freight_value
  - receita_comercial = price

### Fatos de Apoio
- `fact_payments` → receita financeira
- `fact_reviews` → satisfação
- `fact_orders` → ciclo do pedido e SLA

---

## 4. Dimensões

- `dim_date`
- `dim_customers`
- `dim_sellers`
- `dim_products`
- `dim_orders`

---

## 5. Métricas no Power BI

### Vendas
- Receita Comercial
- Receita Financeira
- Ticket médio
- Top produtos e categorias
- Receita por período

### SLA
- Lead time médio
- % atraso
- Atraso por UF e seller

### Reviews
- Nota média
- Distribuição de notas
- Comparação atraso × review

---

## 6. Contrato da Silver

A Silver deve garantir:
- Tipos corretos (datas, números, IDs)
- Integridade relacional
- Regras de sanidade
- Monitoramento de qualidade

---

## 7. Decisões de Negócio

### Receita
- **Comercial**: `order_items.price`
- **Financeira**: `payments.payment_value`
- Mantidas em fatos separadas

### Filtro Global
- Apenas pedidos entregues (`order_status = "delivered"`)

---

## 8. Entregáveis
- Pipeline Bronze → Silver → Gold
- Tabelas Gold prontas para BI
- Dashboard Power BI
- Documentação técnica
