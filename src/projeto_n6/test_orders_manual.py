from pathlib import Path
import pandas as pd
from projeto_n6.run_context import new_run_context
from projeto_n6.paths import build_paths, ensure_run_dirs
from projeto_n6.silver.orders import build_orders_silver
from projeto_n6.io_utils import write_parquet

def main() -> None:
    # 1) Contexto da execução
    ctx = new_run_context()
    paths = build_paths(ctx)
    ensure_run_dirs(paths)

    # 2) Caminho do Bronze (ajuste se necessário)
    bronze_orders = Path(
        "data/bronze/Olist/ingest_date=2026-01-06/olist_orders_dataset.csv"
    )

    # 3) Executa Silver
    df_silver, df_rejects, metrics = build_orders_silver(
        bronze_path=bronze_orders,
        ctx=ctx,
        paths=paths,
    )

    # 4) Visualizações básicas
    print("\n=== METRICS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\n=== SILVER SAMPLE ===")
    print(df_silver.head())

    print("\n=== REJECTS SAMPLE ===")
    print(df_rejects.head())

     

    # 5) Persistência em Parquet
    write_parquet(df_silver, paths.silver_file("orders"))
    write_parquet(df_rejects, paths.rejects_file("orders"))

    # metrics vira DataFrame (1 linha)
    df_metrics = pd.DataFrame([metrics])
    write_parquet(df_metrics, paths.metrics_file())


if __name__ == "__main__":
    main()
