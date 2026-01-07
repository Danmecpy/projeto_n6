from __future__ import annotations

from pathlib import Path
import pandas as pd

from projeto_n6 import paths
from projeto_n6.run_context import new_run_context
from projeto_n6.paths import build_paths, ensure_run_dirs
from projeto_n6.io_utils import write_parquet
from projeto_n6.silver.orders import build_orders_silver
from projeto_n6.logging_utils import setup_logger

def run_pipeline() -> None:
    ctx = new_run_context()
    paths = build_paths(ctx)
    ensure_run_dirs(paths)

    log_file = paths.metrics_dir / "pipeline.log"
    logger = setup_logger("pipeline", log_file)

    try:
        logger.info("Pipeline iniciado")
        logger.info(f"run_id={ctx.run_id}")

        bronze_orders = Path(
            "data/bronze/Olist/ingest_date=2026-01-06/olist_orders_dataset.csv"
        )

        logger.info("Iniciando Silver: orders")

        df_silver, df_rejects, metrics = build_orders_silver(
            bronze_path=bronze_orders,
            ctx=ctx,
            paths=paths,
        )

        logger.info(
            f"Orders Silver concluído | "
            f"rows_in={metrics['rows_in']} | "
            f"rows_valid={metrics['rows_valid']} | "
            f"rows_rejected={metrics['rows_rejected']}"
        )

        reject_ratio = metrics["rows_rejected"] / metrics["rows_in"]
        if reject_ratio > 0.2:
            logger.warning(
                f"Alta taxa de rejeição em orders: {reject_ratio:.2%}"
            )

        write_parquet(df_silver, paths.silver_file("orders"))
        write_parquet(df_rejects, paths.rejects_file("orders"))

        df_metrics = pd.DataFrame([metrics])
        write_parquet(df_metrics, paths.metrics_file())

        logger.info("Pipeline finalizado com sucesso")

    except Exception as exc:
        logger.error("Pipeline falhou", exc_info=exc)
        raise



if __name__ == "__main__":
    run_pipeline()