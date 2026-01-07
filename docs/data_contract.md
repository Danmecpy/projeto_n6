# Data Contract (resumo) — Olist

## Convenções
- **PK**: chave primária (não nula e única)
- **FK**: chave estrangeira (deve existir na tabela referência)
- **Rejects**: registro inválido vai para `data/rejects/...` com:
  `reject_reason`, `reject_rule`, `pipeline_run_id`, `run_timestamp`

## Regra do dashboard (projeto)
KPIs principais usam **apenas `orders.order_status = "delivered"`** (filtro via `dim_orders`).

---

## orders (tabela controladora)
**PK:** `order_id`  
**FK:** `customer_id` → customers.customer_id  
**Campos críticos:** `order_status`, `order_purchase_timestamp`, `order_delivered_customer_date`, `order_estimated_delivery_date` (datas)  
**Regras mínimas (Silver):**
- PK válida (não nula/única)
- `order_status` dentro do domínio esperado
- `order_purchase_timestamp` válido
- se `delivered` → `order_delivered_customer_date` deve existir  
**Reject quando:** PK inválida, status inválido, purchase inválida

---

## order_items (FATO principal — comercial)
**PK:** (`order_id`, `order_item_id`)  
**FKs:** `order_id` → orders.order_id | `product_id` → products.product_id | `seller_id` → sellers.seller_id  
**Campos críticos:** `price`, `freight_value`, `shipping_limit_date`  
**Regras mínimas (Silver):**
- PK composta válida
- `price >= 0`, `freight_value >= 0`
- sem FKs órfãs  
**Reject quando:** PK duplicada/nula, valor < 0, FK órfã

---

## payments (FATO — financeiro)
**PK:** (`order_id`, `payment_sequential`)  
**FK:** `order_id` → orders.order_id  
**Campos críticos:** `payment_type`, `payment_installments`, `payment_value`  
**Regras mínimas (Silver):**
- PK composta válida
- `payment_value >= 0`
- FK não órfã  
**Reject quando:** PK inválida, value < 0, order_id órfão

---

## reviews (FATO — qualidade)
**PK:** `review_id`  
**FK:** `order_id` → orders.order_id  
**Campos críticos:** `review_score`, `review_creation_date`  
**Regras mínimas (Silver):**
- `review_score` entre 1 e 5
- FK não órfã  
**Reject quando:** score fora de 1..5, order_id órfão

---

## customers (DIM)
**PK:** `customer_id`  
**Campos críticos:** `customer_state`, `customer_city`, `customer_zip_code_prefix`  
**Regras mínimas (Silver):**
- PK válida
- `customer_state` padronizado (UF ou nome — escolher 1 padrão)
- city padronizada (trim/case)  
**Reject quando:** PK inválida

---

## products (DIM)
**PK:** `product_id`  
**Campos críticos:** `product_category_name` (opcional), atributos numéricos (peso/dimensões)  
**Regras mínimas (Silver):**
- PK válida
- numéricos coerentes (>= 0 quando aplicável)  
**Reject quando:** PK inválida

---

## sellers (DIM)
**PK:** `seller_id`  
**Campos críticos:** `seller_state`, `seller_city`, `seller_zip_code_prefix`  
**Regras mínimas (Silver):**
- PK válida
- estado/cidade padronizados  
**Reject quando:** PK inválida

---

## category_translation (DIM auxiliar)
**PK lógica:** `product_category_name` (deve ser único)  
**Uso:** apenas para nome legível no dashboard  
**Regras mínimas:** sem duplicidade por categoria (deduplicar se existir)

---

## Métricas operacionais (mínimo por tabela)
Registrar: `rows_in`, `rows_out`, `rows_rejected`, `%rejected`, `pk_duplicates`, `fk_missing_*`, `pipeline_run_id`, `run_timestamp`.
Limite: até 1% ok | 1–5% alerta | >5% erro fatal (revisar)
