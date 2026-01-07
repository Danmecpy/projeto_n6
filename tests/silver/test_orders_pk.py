def test_orders_pk_unique(df_orders_silver):
    pk = df_orders_silver[["order_id", "order_item_id"]]
    assert pk.duplicated().sum() == 0
