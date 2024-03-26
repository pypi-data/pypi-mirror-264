from src.lib.helpers import Symbol
from tests.conftest import graph


def test_symbol():
	step = 0.002
	minimum = 0.2
	maximum = 100
	symbol = Symbol("ETHBTC", step, minimum, maximum, graph_length=10)
	for interval in graph:
		symbol.set_graph_interval(interval, graph[interval])
	assert symbol.symbol == "ETHBTC"
	assert symbol.step == step
	assert symbol.minimum == minimum
	assert symbol.maximum == maximum
	assert symbol.ask is None
	assert symbol.bid is None
	last = {
		"1m": graph["1m"][-1],
		"5m": graph["5m"][-1],
		"1h": graph["1h"][-1],
	}
	last_high_ask = graph["1m"][-1]["high_ask"]
	last_high_bid = graph["1m"][-1]["high_bid"]

	candle = {
		"time": last["1m"]["close_time"] - 1,
		"open_time": last["1m"]["open_time"],
		"close_time": last["1m"]["close_time"],
		"open_ask": last["1m"]["open_ask"],
		"open_bid": last["1m"]["open_bid"],
		"close_ask": last["1m"]["close_ask"] + 1,
		"close_bid": last["1m"]["close_bid"] + 1,
		"high_ask": last["1m"]["close_ask"] + 1,
		"high_bid": last["1m"]["close_bid"] + 1,
		"low_ask": last["1m"]["low_ask"],
		"low_bid": last["1m"]["low_bid"],
		"volume": last["1m"]["low_bid"] + 1,
		"closed": False
	}
	l_1m = len(graph["1m"])
	l_5m = len(graph["5m"])
	l_1h = len(graph["1h"])
	assert graph["1m"][-1]["high_ask"] == last_high_ask
	assert graph["1m"][-1]["high_bid"] == last_high_bid
	symbol.update(candle)
	assert symbol.ask > last_high_ask
	assert symbol.bid > last_high_bid
	assert graph["1m"][-1]["high_ask"] > last_high_ask
	assert graph["1m"][-1]["high_bid"] > last_high_bid
	assert len(graph["1m"]) == l_1m
	assert len(graph["5m"]) == l_5m
	assert len(graph["1h"]) == l_1h
	candle["time"] = last["1m"]["close_time"] + 3600000
	candle["open_time"] = last["1m"]["open_time"] + 3600000
	candle["close_time"] = last["1m"]["close_time"] + 3600000
	symbol.update(candle)
	assert len(graph["1m"]) == l_1m + 1
	assert len(graph["5m"]) == l_5m + 1
	assert len(graph["1h"]) == l_1h + 1
	candle["close_ask"] = 0.00001
	candle["close_bid"] = 0.00001
	symbol.update(candle)
	assert graph["1m"][-1]["low_ask"] == 0.00001
	assert graph["1m"][-1]["low_bid"] == 0.00001
