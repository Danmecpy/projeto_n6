# Silver Design — Projeto Olist

## Objetivo
Transformar dados **Bronze (raw)** em dados **Silver (confiáveis)** para suportar a camada Gold/Power BI.

Silver aplica:
- limpeza / normalização / padronização
- conversão de tipos
- validações de qualidade (PK/FK, regras de domínio)
- sanity checks e métricas operacionais

Silver **não** faz agregações analíticas nem prepara visualizações.

---

## Fato principal e granularidade
**Fato principal:** `olist_order_items_dataset`  
**Granularidade:** 1 linha = 1 item vendido em um pedido (`order_id` + `order_item_id`).

---

## Tabelas consideradas no projeto
### Core (usadas para Gold)
- `olist_orders_dataset` (processo/status + ponte p/ cliente)
- `olist_order_items_dataset` (vendas por item)
- `olist_order_payments_dataset` (receita financeira)
- `olist_order_reviews_dataset` (satisfação)
- `olist_customers_dataset` (cliente)
- `olist_products_dataset` (produto)
- `olist_sellers_dataset` (vendedor)
- `product_category_name_translation` (categoria legível)

### Opcionais
- `olist_geolocation_dataset` (usar somente se houver mapa/geo enriquecida)

---

## Ferramentas (por responsabilidade)
- **Python:** limpeza textual, datas inválidas, conversão de tipos, regras linha a linha, criação de métricas e rejects
- **SQL:** validação relacional (PK/FK), contagens, duplicidades, sanity checks e auditoria

---

## Política de Rejects (quarentena)
Registros que violarem regras da Silver **não são descartados silenciosamente**:
- vão para `data/rejects/...` com motivo e rastreabilidade
- Silver entrega apenas registros aprovados em `data/silver/...`

## MVP (Primeira entrega Silver)

Objetivo do MVP: entregar um primeiro ciclo completo Bronze → Silver → Gold (star schema) → Power BI,
com qualidade e rastreabilidade, evitando escopo excessivo.

### Tabelas no MVP (core)
Estas tabelas são suficientes para responder KPIs de Vendas + SLA + Reviews:

- `orders` (controladora: status + datas + customer_id)
- `order_items` (fato comercial por item)
- `payments` (fato financeiro por pagamento)
- `reviews` (fato de satisfação)
- `customers` (dim cliente)
- `products` (dim produto)
- `sellers` (dim vendedor)

### Tabelas fora do MVP (fase 2)
- `geolocation` (só entra se houver necessidade real de mapa/geo enriquecida)
- `category_translation` (entra se o dashboard precisar de categoria legível; caso contrário pode ser fase 2)

### Saídas do MVP (Parquet)
- `data/silver/olist/run_date=YYYY-MM-DD/<tabela>.parquet`
- `data/rejects/olist/run_date=YYYY-MM-DD/<tabela>_rejects.parquet`
- `data/metrics/olist/run_date=YYYY-MM-DD/metrics.parquet` (métricas operacionais)

---

## Política de Qualidade: ERROR vs REJECT vs WARNING

Para operar como pipeline confiável (padrão corporativo), o projeto classifica problemas de dados em 3 níveis.

### 1) ERROR (falha do pipeline / bloqueia a execução)
Condições que indicam quebra estrutural, risco de gerar dados incorretos ou inconsistência grave.

**Dispara ERROR quando:**
- arquivo/tabela essencial não existe (ex: `orders` ausente)
- schema mudou de forma inesperada (colunas críticas faltando)
- tabela core vazia após leitura (ex: 0 linhas em `order_items`)
- taxa de rejeição acima do limite operacional (ver limites)
- falha de escrita do output Parquet (I/O)

**Ação do pipeline:**
- interromper a execução
- registrar o motivo em log
- não publicar Silver/Gold incompletos

### 2) REJECT (quarentena / não bloqueia)
Erros de dado linha a linha que devem ser removidos do dataset “confiável”, mas preservados para auditoria.

**Regras típicas de REJECT:**
- PK nula ou duplicada
- FK órfã (ex: item com `product_id` inexistente)
- valores monetários inválidos (ex: `payment_value < 0`, `price < 0`)
- `review_score` fora do domínio 1..5
- datas inválidas que impedem uso (ex: purchase_timestamp nulo)

**Ação do pipeline:**
- mover a linha para `rejects` com colunas:
  - `reject_reason`, `reject_rule`, `pipeline_run_id`, `run_timestamp`
- manter apenas linhas aprovadas no Silver

### 3) WARNING (aviso / segue a execução)
Sinais de possível problema que não impedem o uso analítico no MVP, mas devem ser monitorados.

**Exemplos de WARNING:**
- campos descritivos nulos (ex: cidade vazia)
- outliers suspeitos (frete muito alto, peso muito alto) sem regra firme ainda
- inconsistências que não quebram chaves (ex: categoria nula)

**Ação do pipeline:**
- registrar em log e métricas (contagens)
- não rejeitar no MVP (a menos que vire regra futura)

---

## Limites operacionais (guardrails)

- até **1%** rejeição por tabela: normal
- **1% a 5%**: alerta (monitorar no dashboard de pipeline)
- **>5%**: tratar como **ERROR** (revisar regra/ingestão antes de publicar)

Esses limites podem ser ajustados conforme maturidade do pipeline.


### Limites (guardrails)
- até **1%** rejeição: normal
- **1% a 5%**: alerta (monitorar)
- **>5%**: tratar como **erro fatal** (revisar regras/ingestão)

---

## Resultado esperado
Ao final da Silver, os dados devem estar:
- padronizados e tipados corretamente
- com integridade relacional garantida (PK/FK)
- com rastreabilidade (métricas + rejects)
- prontos para a Gold (modelo estrela no Power BI)

