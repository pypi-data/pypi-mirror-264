# -*- coding: utf-8 -*-
from uuid import uuid4


class Side:
	BUY = 1
	SELL = 0


class Symbol:
	def __init__(self, symbol: str, step=0.01, minimum=0.01, maximum=.0, graph_length=1000):
		self.__symbol = symbol
		self.__step = step
		self.__minimum = minimum
		self.__maximum = maximum
		self.__intervals = []
		self.__graph = {}
		self.__graph_length = graph_length
		self.__ask = None
		self.__bid = None

	def set_graph_interval(self, interval, graph):
		self.__intervals.append(interval)
		self.__graph[interval] = graph

	def update(self, candle):
		self.__ask = candle["close_ask"]
		self.__bid = candle["close_bid"]
		closed = candle.pop("closed", False)
		for interval in self.__intervals:
			last = self.__graph[interval][-1]
			if candle["open_time"] > last["close_time"] and not closed:
				self.__create_candle(last, candle, interval)
				if interval == self.__intervals[0]:
					self.__update_volume(last)
				if len(self.__graph[interval]) > self.__graph_length:
					self.__graph[interval] = self.__graph[interval][1:]
			else:
				self.__update_candle(last, candle, interval)

	def __update_volume(self, last):
		for interval in self.__intervals[1:]:
			self.__graph[interval][-1]["volume"] += last["volume"]

	def __create_candle(self, last, new, interval):
		self.__graph[interval].append({
			"open_time": new["open_time"],
			"close_time": new["open_time"] + (last["close_time"] - last["open_time"]),
			"open_ask": new["open_ask"],
			"open_bid": new["open_bid"],
			"close_ask": new["close_ask"],
			"close_bid": new["close_bid"],
			"high_ask": new["high_ask"],
			"high_bid": new["high_bid"],
			"low_ask": new["low_ask"],
			"low_bid": new["low_bid"],
			"volume": new["volume"]
		})

	def __update_candle(self, last, new, interval):
		if interval == self.__intervals[0]:
			last["volume"] = new["volume"]
		last["close_ask"] = new["close_ask"]
		last["close_bid"] = new["close_bid"]
		if last["close_ask"] > last["high_ask"]:
			last["high_ask"] = new["close_ask"]
		elif last["close_ask"] < last["low_ask"]:
			last["low_ask"] = new["close_ask"]
		if last["close_bid"] > last["high_bid"]:
			last["high_bid"] = new["close_bid"]
		elif last["close_bid"] < last["low_bid"]:
			last["low_bid"] = new["close_bid"]

	@property
	def symbol(self):
		return self.__symbol

	@property
	def step(self):
		return self.__step

	@property
	def minimum(self):
		return self.__minimum

	@property
	def maximum(self):
		return self.__maximum

	@property
	def ask(self):
		return self.__ask

	@property
	def bid(self):
		return self.__bid


class Order:
	NEW = 0
	PARTIALLY_FILLED = 1
	FILLED = 2
	CANCELED = 3
	REJECTED = 4
	EXPIRED = 5

	def __init__(self, order_id, side, symbol, price, amount, filled=.0, status=.0):
		self.__id = order_id
		self.__side = side
		self.__symbol = symbol
		self.__price = price
		self.__amount = amount
		self.__filled = filled
		self.__status = status or Order.NEW

	def update(self, status, filled: float):
		self.__status = status
		self.__filled = filled

	@property
	def id(self):
		return self.__id

	@property
	def side(self):
		return self.__side

	@property
	def symbol(self):
		return self.__symbol

	@property
	def price(self):
		return self.__price

	@property
	def amount(self):
		return self.__amount

	@property
	def filled(self):
		return self.__filled

	@property
	def status(self):
		return self.__status


class Position:
	def __init__(self, open_order: Order, close_price=.0, position_id=None):
		self.__id = position_id or str(uuid4())
		self.__open_order = open_order
		self.__close_order = None
		self.__close_price = close_price

	def update_close_price(self, close_price: float):
		self.__close_price = close_price

	def update_close_order(self, close_order: Order):
		self.__close_order = close_order

	@property
	def id(self):
		return self.__id

	@property
	def side(self):
		return self.__open_order.side

	@property
	def symbol(self):
		return self.__open_order.symbol

	@property
	def open_order(self):
		return self.__open_order

	@property
	def close_price(self):
		return self.__close_price

	@property
	def close_order(self):
		return self.__close_order
