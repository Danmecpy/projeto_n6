from pathlib import Path
import shutil
from datetime import date, datetime
from projeto_n6.run_context import RunContext
from projeto_n6.pipeline import run_pipeline

def test_pipeline_runs_without_error(tmp_path, monkeypatch):
    from datetime import date, datetime
    from projeto_n6.run_context import RunContext
    from projeto_n6.pipeline import run_pipeline

    monkeypatch.chdir(tmp_path)

    ctx = RunContext(
        run_id="test_run",
        run_date=date(2026, 1, 6),
        run_ts=datetime(2026, 1, 6, 0, 0, 0),
    )

    bronze_dir = (
        tmp_path
        / "data"
        / "bronze"
        / "Olist"
        / f"ingest_date={ctx.run_date.isoformat()}"
    )
    bronze_dir.mkdir(parents=True)

    (bronze_dir / "olist_orders_dataset.csv").write_text(
        "order_id,customer_id,order_status,order_purchase_timestamp\n"
        "o1,c1,delivered,2020-01-01\n"
    )

    run_pipeline()
