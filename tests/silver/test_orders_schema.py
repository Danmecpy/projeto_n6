def test_orders_pk_not_null(df_orders_silver):
    assert df_orders_silver["order_id"].isna().sum() == 0
    assert df_orders_silver["order_item_id"].isna().sum() == 0
    
    