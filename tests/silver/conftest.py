import pandas as pd
import pytest


@pytest.fixture
def df_orders_silver():
    """
    Fixture de dados Silver válida para testes.
    Representa a saída esperada da camada Silver.
    """

    return pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_item_id": [1, 1],
            "product_id": ["p1", "p2"],
            "seller_id": ["s1", "s2"],
            "price": [100.0, 250.0],
            "freight_value": [10.0, 20.0],
        }
    )
