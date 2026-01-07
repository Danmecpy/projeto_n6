from pathlib import Path
import shutil

from projeto_n6.pipeline import run_pipeline

def test_pipeline_runs_without_error(tmp_path, monkeypatch):
    # Arrange
    data_dir = tmp_path / "data"
    bronze_dir = data_dir / "bronze" / "olist"
    bronze_dir.mkdir(parents=True)

    orders_file = bronze_dir / "olist_orders_dataset.csv"
    orders_file.write_text(
        "order_id,customer_id,order_status,order_purchase_timestamp\n"
        "o1,c1,delivered,2020-01-01\n"
    )

    # Monkeypatch data directory
    monkeypatch.chdir(tmp_path)

    # Act / Assert
    run_pipeline()

    # Verify output exists
    assert (tmp_path / "data" / "silver").exists()
    assert (tmp_path / "data" / "metrics").exists()
