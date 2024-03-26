from asyncio import get_event_loop
from src import load_exchange
from src.binance import Binance
from src.lib.exchange import Exchange


def test_exchange_load():
	assert load_exchange("binance") == Binance


def test_exchange_load_invalid():
	ex = False
	try:
		load_exchange("invalid_exchange")
	except NotImplementedError:
		ex = True
	assert ex is True


def test_not_implemented():
	def try_not_implemented(function, *args):
		ni = False
		try:
			function(*args)
		except NotImplementedError:
			ni = True
		assert ni is True

	async def a_try_not_implemented(function, *args):
		ni = False
		try:
			await function(*args)
		except NotImplementedError:
			ni = True
		assert ni is True

	try_not_implemented(Exchange.get_symbols, "", [])
	try_not_implemented(Exchange.get_intervals, "")
	try_not_implemented(Exchange.get_funds, "")
	try_not_implemented(Exchange.get_graph_interval, "", "", "")
	try_not_implemented(Exchange.create_order, "", 1, "", 0, 0)
	try_not_implemented(Exchange.check_order, "", 1)
	try_not_implemented(Exchange.cancel_order, "", 1)

	loop = get_event_loop()
	loop.run_until_complete(a_try_not_implemented(Exchange.subscribe, "", try_not_implemented))
