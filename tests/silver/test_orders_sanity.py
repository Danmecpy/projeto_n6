def test_orders_price_positive(df_orders_silver):
    assert (df_orders_silver["price"] > 0).all()
