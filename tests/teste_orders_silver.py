import pandas as pd
from pathlib import Path

from projeto_n6.run_context import new_run_context
from projeto_n6.paths import build_paths
from projeto_n6.silver.orders import build_orders_silver


def test_orders_silver_returns_expected_objects(tmp_path):
    # Arrange
    data = {
        "order_id": ["o1", "o2", "o2"],
        "customer_id": ["c1", "c2", "c2"],
        "order_status": ["delivered", "delivered", "invalid"],
        "order_purchase_timestamp": [
            "2020-01-01",
            "2020-01-02",
            "invalid_date",
        ],
    }
    df = pd.DataFrame(data)

    bronze_file = tmp_path / "orders.csv"
    df.to_csv(bronze_file, index=False)

    ctx = new_run_context()
    paths = build_paths(ctx)

    # Act
    df_silver, df_rejects, metrics = build_orders_silver(
        bronze_path=bronze_file,
        ctx=ctx,
        paths=paths,
    )

    # Assert
    assert isinstance(df_silver, pd.DataFrame)
    assert isinstance(df_rejects, pd.DataFrame)
    assert isinstance(metrics, dict)


def test_orders_silver_pk_duplicate_goes_to_reject(tmp_path):
    data = {
        "order_id": ["o1", "o1"],
        "customer_id": ["c1", "c1"],
        "order_status": ["delivered", "delivered"],
        "order_purchase_timestamp": ["2020-01-01", "2020-01-01"],
    }
    df = pd.DataFrame(data)

    bronze_file = tmp_path / "orders.csv"
    df.to_csv(bronze_file, index=False)

    ctx = new_run_context()
    paths = build_paths(ctx)

    df_silver, df_rejects, metrics = build_orders_silver(
        bronze_path=bronze_file,
        ctx=ctx,
        paths=paths,
    )

    assert metrics["pk_duplicate_count"] == 1
    assert len(df_silver) == 1
    assert len(df_rejects) == 1


def test_orders_silver_metrics_consistency(tmp_path):
    data = {
        "order_id": ["o1", "o2"],
        "customer_id": ["c1", "c2"],
        "order_status": ["delivered", "invalid"],
        "order_purchase_timestamp": ["2020-01-01", "2020-01-02"],
    }
    df = pd.DataFrame(data)

    bronze_file = tmp_path / "orders.csv"
    df.to_csv(bronze_file, index=False)

    ctx = new_run_context()
    paths = build_paths(ctx)

    _, _, metrics = build_orders_silver(
        bronze_path=bronze_file,
        ctx=ctx,
        paths=paths,
    )

    assert metrics["rows_in"] == 2
    assert metrics["rows_valid"] + metrics["rows_rejected"] == 2
