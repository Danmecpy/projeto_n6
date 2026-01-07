from __future__ import annotations

import pandas as pd
from pathlib import Path

from projeto_n6.run_context import RunContext
from projeto_n6.paths import PipelinePaths


def build_orders_silver(
    bronze_path: Path,
    ctx: RunContext,
    paths: PipelinePaths,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Constrói a tabela Silver de orders.

    Retorna:
    - df_silver: dados válidos
    - df_rejects: registros rejeitados
    - metrics: métricas da execução
    """

    # ---------------------------------------------------------------------
    # 1) Verificar se o arquivo Bronze existe
    # ---------------------------------------------------------------------
    if not bronze_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {bronze_path}")

    # ---------------------------------------------------------------------
    # 2) Ler dados da Bronze
    # ---------------------------------------------------------------------
    df = pd.read_csv(bronze_path)
    rows_in = len(df)

    # ---------------------------------------------------------------------
    # 3) Validar colunas obrigatórias
    # ---------------------------------------------------------------------
    required_columns = {
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")

    # Trabalhar sempre com cópia
    df = df.copy()

    # ---------------------------------------------------------------------
    # 4) Normalização de tipos
    # ---------------------------------------------------------------------
    df["order_id"] = df["order_id"].astype(str)
    df["customer_id"] = df["customer_id"].astype(str)
    df["order_status"] = df["order_status"].astype(str)

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce",
    )

    # ---------------------------------------------------------------------
    # 5) Regras de Qualidade (Data Quality Rules)
    # ---------------------------------------------------------------------

    # PK inválida
    pk_null_mask = df["order_id"].isna() # serve para detectar nulos
    pk_duplicate_mask = df["order_id"].duplicated(keep="first") # serve para detectar duplicados

    # Status inválido
    valid_status = {
        "delivered",
        "shipped",
        "processing",
        "canceled",
        "unavailable",
    }
    invalid_status_mask = ~df["order_status"].isin(valid_status)

    # Data inválida
    invalid_date_mask = df["order_purchase_timestamp"].isna()

    # ---------------------------------------------------------------------
    # 6) Máscara final de rejeição (OU lógico)
    # ---------------------------------------------------------------------
    reject_mask = (
        pk_null_mask
        | pk_duplicate_mask
        | invalid_status_mask
        | invalid_date_mask
    )

    # ---------------------------------------------------------------------
    # 7) Separar dados válidos e rejeitados
    # ---------------------------------------------------------------------
    df_rejects = df[reject_mask].copy() 
    df_silver = df[~reject_mask].copy()

    # ---------------------------------------------------------------------
    # 8) Métricas da execução
    # ---------------------------------------------------------------------
    metrics = {
        "table": "orders",
        "run_id": ctx.run_id,
        "run_date": ctx.run_date.isoformat(),

        "rows_in": rows_in,
        "rows_valid": len(df_silver),
        "rows_rejected": len(df_rejects),

        "pk_null_count": int(pk_null_mask.sum()),
        "pk_duplicate_count": int(pk_duplicate_mask.sum()),
        "invalid_status_count": int(invalid_status_mask.sum()),
        "invalid_date_count": int(invalid_date_mask.sum()),
    }

    # ---------------------------------------------------------------------
    # 9) Retorno padrão da Silver
    # ---------------------------------------------------------------------
    return df_silver, df_rejects, metrics
