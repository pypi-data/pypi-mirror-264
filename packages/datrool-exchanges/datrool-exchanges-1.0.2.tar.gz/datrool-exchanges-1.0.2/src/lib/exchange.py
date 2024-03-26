# -*- coding: utf-8 -*-
from typing import Callable, Coroutine


class Exchange:
	def __init__(self, name, symbols=[], intervals=[]):
		self._name = name
		self._intervals = intervals or self.get_intervals()
		self._symbols = self.get_symbols(symbols)
		self._funds = self.get_funds()
		self._orders = {}
		self.retry_limit = 0

	def get_symbols(self, symbols: list):
		raise NotImplementedError()

	def get_intervals(self):
		raise NotImplementedError()

	def get_funds(self):
		raise NotImplementedError

	def get_graph_interval(self, symbol, interval, length=1000, raw=False):
		raise NotImplementedError

	def get_graph(self, symbol, intervals=None, length=1000, raw=False):
		graph = {}
		intervals = intervals or self._intervals
		for interval in intervals:
			graph[interval] = self.get_graph_interval(symbol, interval, length=length, raw=raw)
		return graph

	async def subscribe(self, callback: Callable[..., Coroutine], raw=False):
		raise NotImplementedError

	def create_order(self, side, symbol, amount, price):
		raise NotImplementedError

	def check_order(self, order_id):
		raise NotImplementedError

	def cancel_order(self, order_id):
		raise NotImplementedError

	@property
	def name(self):
		return self._name

	@property
	def symbols(self):
		return list(self._symbols.keys())

	@property
	def intervals(self):
		return self._intervals

	@property
	def funds(self):
		return self._funds
