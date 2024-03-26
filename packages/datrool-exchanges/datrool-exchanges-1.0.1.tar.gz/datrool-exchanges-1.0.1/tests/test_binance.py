from os import environ
from json import loads
from asyncio import get_event_loop
from dotenv import load_dotenv
from src.binance import Binance
from src.lib.helpers import Order, Side
load_dotenv()


credentials = {
	"API_KEY": environ.get("BINANCE_API_KEY"),
	"SECRET_KEY": environ.get("BINANCE_SECRET_KEY").encode()
}


def test_binance_graph():
	b = Binance(intervals=["1m", "5m", "1h"])
	assert len(b._symbols.keys()) > 0
	graph = b.get_graph("ETHBTC", ["1m", "5m", "1h"])
	assert "1m" in graph
	assert "5m" in graph
	assert "1h" in graph
	symbol = b._symbols["ETHBTC"]
	assert symbol._Symbol__graph == graph


def test_binance_graph_raw():
	b = Binance(symbols=["ETHBTC"], intervals=["1m"])
	graph = b.get_graph("ETHBTC", ["1m"])
	raw_graph = b.get_graph("ETHBTC", ["1m"], raw=True)
	assert raw_graph != graph
	assert b.name == "binance"
	assert b.symbols == ["ETHBTC"]
	assert b.intervals == ["1m"]
	assert isinstance(b.funds, dict)


def test_binance_graph_invalid():
	b = Binance()
	b.retry_limit = 2
	graph = b.get_graph("ethbtc", ["1m"])
	assert graph["1m"] == []


def test_binance_stream():
	b = Binance(symbols=["ETHBTC"], intervals=["1m"])
	b.get_graph("ETHBTC")

	called = []

	async def callback(symbol):
		called.append(1)
		b.exit_stream()

	loop = get_event_loop()
	loop.run_until_complete(b.subscribe(callback))

	assert len(called) == 1

	async def raw_callback(data):
		data = loads(data)
		assert "stream" in data
		assert "data" in data
		called.append(1)
		b.exit_stream()

	loop = get_event_loop()
	loop.run_until_complete(b.subscribe(raw_callback, raw=True))

	assert len(called) == 2


def test_binance_stream_failed():
	wss = Binance._Binance__stream
	Binance._Binance__stream = "wss://127.0.0.1/jezevec/stream"

	b = Binance(symbols=["ETHBTC"], intervals=["1m"])
	b.get_graph("ETHBTC")
	b.retry_limit = 2

	called = []

	async def callback(symbol):
		pass

	loop = get_event_loop()
	loop.run_until_complete(b.subscribe(callback))

	assert len(called) == 0

	Binance._Binance__stream = wss


def test_binance_trade():
	b = Binance(symbols=["BTCUSDT"], intervals=["1m"], credentials=credentials)
	graph = b.get_graph("BTCUSDT")

	price = graph["1m"][-1]["close_ask"] - 10000
	order = b.buy("BTCUSDT", price, float(b._funds["USDT"]["free"]) / 20, quoted_amount=True)
	status = order.status
	oid = order.id

	b.check_order(order.id)
	canceled = b.cancel_order(order.id)

	assert status == Order.NEW
	assert order.status == Order.CANCELED
	assert oid == order.id
	assert canceled is True

	price = graph["1m"][-1]["close_ask"] + 10000
	order = b.sell("BTCUSDT", price, float(b._funds["USDT"]["free"]) / 20, quoted_amount=True)
	status = order.status
	oid = order.id

	b.check_order(order.id)
	canceled = b.cancel_order(order.id)

	assert status == Order.NEW
	assert order.status == Order.CANCELED
	assert oid == order.id
	assert canceled is True


def test_binance_trade_invalid():
	b = Binance(symbols=["BTCUSDT"], intervals=["1m"], credentials=credentials)
	endpoint = b._Binance__endpoint

	order = b.buy("BTCUSDT", 1000, 1)
	assert order is None
	check = b.check_order("3232")
	assert check == False
	canceled = b.cancel_order("3232")
	assert canceled == False

	graph = b.get_graph("BTCUSDT")
	price = graph["1m"][-1]["close_ask"] - 10000
	order = b.buy("BTCUSDT", price, float(b._funds["USDT"]["free"]) / 20, quoted_amount=True)
	b._Binance__endpoint = "https://127.0.0.1/jezevec/api/V0/"

	check = b.check_order(order.id)
	assert check == False
	canceled = b.cancel_order(order.id)
	assert canceled == False

	b._Binance__endpoint = endpoint
	check = b.cancel_order(order.id)
	assert check == True


def test_binance_position():
	b = Binance(symbols=["BTCUSDT"], intervals=["1m"], credentials=credentials)
	graph = b.get_graph("BTCUSDT")

	price = graph["1m"][-1]["close_ask"] - 10000
	position = b.open_position(
		Side.BUY, "BTCUSDT", price, float(b._funds["USDT"]["free"]) / 20, quoted_amount=True
	)
	assert position is not None
	p = b.get_position(position.id)
	assert p is not None
	b.close_position(position.id)
	b.check_position(position.id)

	price = graph["1m"][-1]["close_ask"] + 10000
	position = b.open_position(
		Side.BUY, "BTCUSDT", price, float(b._funds["USDT"]["free"]) / 20, quoted_amount=True
	)
	assert position is not None
	b.close_position(position.id, graph["1m"][-1]["close_ask"] - 10000)
	b.check_position(position.id)

	closed_positions = b.flush_closed_positions()
	assert len(closed_positions.keys()) == 2

	symbol = b._symbols["BTCUSDT"]
	symbol._Symbol__ask = graph["1m"][-1]["close_ask"]
	symbol._Symbol__bid = graph["1m"][-1]["close_ask"]
	price = graph["1m"][-1]["close_ask"] + 10000
	position = b.open_position(
		Side.BUY, "BTCUSDT", price, float(b._funds["USDT"]["free"]) / 20,
		quoted_amount=True, close_price=price - 20000
	)
	assert position is not None
	assert position.open_order.status == Order.FILLED
	b.check_position(position.id)
	assert position.close_order is not None
	assert position.close_order.status == Order.FILLED
	closed_positions = b.flush_closed_positions()
	assert len(closed_positions.keys()) == 0
	b.check_position(position.id)
	closed_positions = b.flush_closed_positions()
	assert len(closed_positions.keys()) == 1


def test_binance_position_invalid():
	b = Binance(symbols=["BTCUSDT"], intervals=["1m"], credentials=credentials)

	pos = b.open_position(Side.BUY, "BTCUSDT", 10000, 10)
	assert pos is None

	pos = b.check_position("453245254")
	assert pos == False

	pos = b.close_position("453245254")
	assert pos == False
