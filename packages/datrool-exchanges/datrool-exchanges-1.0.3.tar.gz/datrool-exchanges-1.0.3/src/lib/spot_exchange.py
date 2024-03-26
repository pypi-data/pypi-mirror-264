# -*- coding: utf-8 -*-
from .position_exchange import PositionExchange
from .helpers import Side


class SpotExchange(PositionExchange):
	def __init__(self, name, symbols=[], intervals=[], logger=None):
		self.__positions = {}
		self.__positions_closed = {}
		super().__init__(name, symbols, intervals, logger)

	def buy(self, symbol, price, amount, quoted_amount=False):
		if quoted_amount:
			amount = amount / price
		return self.create_order(Side.BUY, symbol, amount, price)

	def sell(self, symbol, price, amount, quoted_amount=False):
		if quoted_amount:
			amount = amount / price
		return self.create_order(Side.SELL, symbol, amount, price)
