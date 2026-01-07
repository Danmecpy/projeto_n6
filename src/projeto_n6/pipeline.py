from __future__ import annotations

from pathlib import Path
import pandas as pd

from projeto_n6.run_context import new_run_context
from projeto_n6.paths import build_paths, ensure_run_dirs
from projeto_n6.io_utils import write_parquet
from projeto_n6.silver.orders import build_orders_silver


def run_pipeline() -> None:
    """
    Executa o pipeline Silver do projeto.
    """


ctx = new_run_context() # contexto da execução para controle de versões e auditoria
paths = build_paths(ctx) # constrói os caminhos de diretórios e arquivos
ensure_run_dirs(paths) # garante que os diretórios existem


bronze_orders = Path(
    "data/bronze/Olist/ingest_date=2026-01-06/olist_orders_dataset.csv"
)  # caminho do arquivo Bronze de orders

df_silver, df_rejects, metrics = build_orders_silver(
   bronze_path=bronze_orders,
   ctx=ctx,
   paths=paths,)

#a pipeline foi executada, agora vamos salvar os resultados
write_parquet(df_silver, paths.silver_file("orders"))
write_parquet(df_rejects, paths.rejects_file("orders"))
# metrics vira DataFrame (1 linha)
df_metrics = pd.DataFrame([metrics])
write_parquet(df_metrics, paths.metrics_file())


if __name__ == "__main__":
    run_pipeline()