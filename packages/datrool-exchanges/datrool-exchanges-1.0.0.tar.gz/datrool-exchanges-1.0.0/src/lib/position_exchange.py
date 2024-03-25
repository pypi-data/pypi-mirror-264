# -*- coding: utf-8 -*-
from .exchange import Exchange
from .helpers import Order as O, Position, Side


class PositionExchange(Exchange):
	def __init__(self, name, symbols=[], intervals=[]):
		self.__positions = {}
		self.__positions_closed = {}
		super().__init__(name, symbols, intervals)

	def open_position(self, side, symbol, price, amount, quoted_amount=False, close_price=0):
		if quoted_amount:
			amount = amount / price
		order = self.create_order(side, symbol, amount, price)
		if order:
			position = Position(order, close_price)
			self.__positions[position.id] = position
			return position
		return None

	def close_position(self, position_id, price=0) -> bool:
		if position_id not in self.__positions:
			return False
		position = self.__positions[position_id]

		if position.open_order.status != O.FILLED:
			self.cancel_order(position.open_order.id)
		side = Side.SELL if position.side == Side.BUY else Side.BUY
		if position.open_order.filled:
			order = self.create_order(side, position.symbol, position.open_order.filled, price)
			position.update_close_order(order)
		return True

	def check_position(self, position_id) -> bool:
		if position_id not in self.__positions:
			return False
		pos = self.__positions[position_id]
		if (
			pos.open_order.status in [O.CANCELED, O.REJECTED, O.EXPIRED] or
			(pos.close_order and pos.close_order.status == O.FILLED)
		):
			self.__positions_closed[position_id] = self.__positions.pop(position_id)
		elif pos.close_price and (
			(pos.side == Side.BUY and pos.close_price <= self._symbols[pos.symbol].bid) or
			(pos.side == Side.SELL and pos.close_price >= self._symbols[pos.symbol].ask)
		):
			self.close_position(position_id, price=pos.close_price)
		return True

	def get_position(self, id):
		return self.__positions.get(id)

	def flush_closed_positions(self):
		flush = self.__positions_closed
		self.__positions_closed = {}
		return flush
