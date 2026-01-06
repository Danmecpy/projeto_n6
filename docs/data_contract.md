# Data Contract — Projeto Olist (Bronze → Silver → Gold)

## 0) Convenções
- **PK** = Primary Key (chave primária): identifica linha de forma única (não nula e sem duplicatas)
- **FK** = Foreign Key (chave estrangeira): referencia a PK de outra tabela (não pode gerar órfãos)
- **Rejects**: registros inválidos vão para quarentena com motivo (não somem do pipeline)

## 1) Tabelas Core (usadas na Gold)

---

## 1.1 olist_orders_dataset (dim/processo)
**Papel:** tabela de processo do pedido (ponte para customer + status + datas do ciclo)

### PK
- `order_id`

### FKs
- `customer_id` → `olist_customers_dataset.customer_id`

### Campos críticos (tipos esperados)
- `order_purchase_timestamp` (datetime)
- `order_approved_at` (datetime, pode ser nulo)
- `order_delivered_carrier_date` (datetime, pode ser nulo)
- `order_delivered_customer_date` (datetime, pode ser nulo)
- `order_estimated_delivery_date` (datetime)
- `order_status` (string)

### Regras Silver (mínimas)
- PK `order_id` não nula e única
- `order_status` dentro do conjunto esperado (domínio controlado)
- sanity check: `order_purchase_timestamp` não deve ser nulo
- sanity check (quando entregue): se `order_status = delivered`, então `order_delivered_customer_date` deve existir
- sanity check: `order_purchase_timestamp <= order_estimated_delivery_date` (quando aplicável)

**Reject quando:**
- `order_id` nulo/duplicado
- `order_purchase_timestamp` inválido/nulo
- status inválido

---

## 1.2 olist_order_items_dataset (fact principal - comercial)
**Papel:** itens vendidos (base para volume e receita comercial)

### PK (composta)
- (`order_id`, `order_item_id`)

### FKs
- `order_id` → `olist_orders_dataset.order_id`
- `product_id` → `olist_products_dataset.product_id`
- `seller_id` → `olist_sellers_dataset.seller_id`

### Campos críticos (tipos esperados)
- `shipping_limit_date` (datetime ou date)
- `price` (numeric)
- `freight_value` (numeric)

### Regras Silver (mínimas)
- PK composta não nula e única
- `price >= 0`
- `freight_value >= 0`
- FKs não podem gerar órfãos (order/product/seller devem existir)

**Reject quando:**
- PK duplicada
- `price < 0` ou `freight_value < 0`
- FK órfã (product/seller/order inexistente)

---

## 1.3 olist_order_payments_dataset (fact financeiro)
**Papel:** pagamentos (base para receita financeira)

### PK (composta)
- (`order_id`, `payment_sequential`)

### FKs
- `order_id` → `olist_orders_dataset.order_id`

### Campos críticos (tipos esperados)
- `payment_type` (string)
- `payment_installments` (int)
- `payment_value` (numeric)

### Regras Silver (mínimas)
- PK composta não nula e única
- `payment_value >= 0`
- FK `order_id` deve existir em orders
- `payment_installments >= 0`

**Reject quando:**
- `order_id` inexistente em orders
- `payment_value < 0`
- PK duplicada

---

## 1.4 olist_order_reviews_dataset (fact qualidade)
**Papel:** reviews (satisfação; usado com entregues)

### PK
- `review_id` (se houver duplicidade, tratar como erro)

### FKs
- `order_id` → `olist_orders_dataset.order_id`

### Campos críticos (tipos esperados)
- `review_score` (int)
- `review_creation_date` (datetime/date)
- `review_answer_timestamp` (datetime/date, pode ser nulo)

### Regras Silver (mínimas)
- `review_score` entre 1 e 5
- FK `order_id` deve existir em orders

**Reject quando:**
- `review_score` fora de 1..5
- `order_id` órfão

---

## 1.5 olist_customers_dataset (dim)
**Papel:** dados do cliente (localidade e identificadores)

### PK
- `customer_id`

### Campos críticos
- `customer_unique_id` (string)
- `customer_zip_code_prefix` (string/num)
- `customer_city` (string)
- `customer_state` (string)

### Regras Silver (mínimas)
- PK não nula e única
- `customer_state` válido (UF ou nome padronizado — escolha um padrão e aplique)
- `customer_city` padronizado (trim/case; remover caracteres estranhos se necessário)

**Reject quando:**
- `customer_id` nulo/duplicado

---

## 1.6 olist_products_dataset (dim)
**Papel:** atributos do produto

### PK
- `product_id`

### Campos críticos
- `product_category_name` (string, pode ser nulo)
- atributos numéricos (peso/dimensões) como numeric (quando presentes)

### Regras Silver (mínimas)
- PK não nula e única
- campos numéricos coerentes (ex: peso >= 0)

**Reject quando:**
- `product_id` nulo/duplicado

---

## 1.7 olist_sellers_dataset (dim)
**Papel:** dados do vendedor

### PK
- `seller_id`

### Campos críticos
- `seller_zip_code_prefix` (string/num)
- `seller_city` (string)
- `seller_state` (string)

### Regras Silver (mínimas)
- PK não nula e única
- `seller_state` válido e padronizado
- `seller_city` padronizado

**Reject quando:**
- `seller_id` nulo/duplicado

---

## 1.8 product_category_name_translation (dim auxiliar)
**Papel:** traduzir categoria para nome legível (ex: PT → EN)

### PK sugerida (lógica)
- `product_category_name` (deve ser único)

### Regras Silver
- `product_category_name` não deve repetir (se repetir, escolher regra: deduplicar por prioridade)
- campos textuais padronizados

---

## 2) Tabela Opcional

## 2.1 olist_geolocation_dataset (dim geo)
**Papel:** enriquecer geo (lat/lng). Grande e com alta duplicidade por CEP.

### Observações
- Pode existir múltiplas linhas por `geolocation_zip_code_prefix` (isso não é necessariamente erro)
- Usar somente se houver necessidade real (mapa/geo)

### Regras Silver (mínimas)
- lat/lng numéricos e dentro de limites plausíveis
- texto de cidade/estado padronizado

---

## 3) Métricas operacionais (mínimas por tabela)
Para cada tabela Silver, registrar:
- `rows_in`, `rows_out`, `rows_rejected`, `%rejected`
- `pk_nulls`, `pk_duplicates`
- `fk_missing_<tabela>` (contagem por relação)
- `pipeline_run_id`, `run_timestamp`

---

## 4) Regra do projeto para métricas no Power BI
Para comparabilidade entre Receita e Reviews:
- métricas principais consideram **apenas pedidos com `order_status = "delivered"`**
- a filtragem deve ocorrer via `dim_orders` (tabela controladora)
