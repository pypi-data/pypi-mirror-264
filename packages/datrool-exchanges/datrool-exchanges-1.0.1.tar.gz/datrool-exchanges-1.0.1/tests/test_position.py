from src.lib.helpers import Order, Position, Side


def test_order():
	symbol = "ETHBTC"
	side = Side.BUY
	order = Order(1, side, symbol, 20, 10)
	assert order.side == side
	assert order.symbol == symbol
	assert order.id == 1
	assert order.price == 20
	assert order.amount == 10
	assert order.filled == 0
	assert order.status == Order.NEW

	order.update(Order.PARTIALLY_FILLED, 5)
	assert order.filled == 5
	assert order.status == Order.PARTIALLY_FILLED


def test_position():
	symbol = "ETHBTC"
	side = Side.BUY
	order = Order(1, side, symbol, 20, 10)
	close_price = 10
	position = Position(order, close_price)
	assert len(position.id) > 0
	assert position.symbol == symbol
	assert position.open_order == order
	assert position.side == side
	assert position.close_order is None
	assert position.close_price == close_price

	close_price = 12
	position.update_close_price(close_price)
	assert position.close_price == 12

	side = Side.SELL
	order = Order(1, side, symbol, 30, 10)
	position.update_close_order(order)
	assert position.close_order == order
