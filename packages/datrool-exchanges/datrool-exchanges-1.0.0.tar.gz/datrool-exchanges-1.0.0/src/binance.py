# -*- coding: utf-8 -*-
from time import time, sleep
from math import floor
from hmac import new
from hashlib import sha256
from urllib.request import Request, urlopen
from orjson import loads
from websockets import connect
from .lib.spot_exchange import SpotExchange
from .lib.helpers import Symbol, Order, Side


class Binance(SpotExchange):
	__endpoint = "https://api.binance.com/api/v3/"
	__stream = "wss://stream.binance.com:9443/stream"

	ORDER_STATES = {
		"NEW": Order.NEW,
		"PARTIALLY_FILLED": Order.PARTIALLY_FILLED,
		"FILLED": Order.FILLED,
		"CANCELED": Order.CANCELED,
		"PENDING_CANCEL": Order.CANCELED,
		"REJECTED": Order.REJECTED,
		"EXPIRED": Order.EXPIRED,
		"EXPIRED_IN_MATCH": Order.EXPIRED,
	}

	def __init__(self, symbols=[], intervals=[], credentials={}):
		self.__credentials = credentials
		self.__exit_stream = False
		super().__init__("binance", symbols, intervals)

	def get_symbols(self, symbols=[]):
		result = {}
		if data := self._http_request("exchangeInfo", method="GET"):
			for symbol in data["symbols"]:
				if symbols and symbol["symbol"] not in symbols:
					continue
				for filter in symbol["filters"]:
					if filter["filterType"] == "LOT_SIZE":
						result[symbol["symbol"]] = Symbol(
							symbol=symbol["symbol"],
							step=len(filter["stepSize"].replace(".", "").split("1")[0]),
							minimum=float(filter["minQty"]),
							maximum=float(filter["maxQty"])
						)
						break
		return result

	def get_intervals(self):
		return [
			"1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h",
			"4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"
		]

	def get_funds(self):
		data = self._http_request("account", method="GET", auth=True)
		if not data or "balances" not in data:
			return {}
		funds = {}
		for balance in data["balances"]:
			if float(balance["free"]):
				funds[balance["asset"]] = {
					"free": balance["free"],
					"locked": balance["locked"]
				}
		return funds

	def create_order(self, side, symbol, amount, price):
		data = {
			"symbol": symbol,
			"side": "BUY" if side == Side.BUY else "SELL",
			"type": "LIMIT",
			"timeInForce": "GTC",
			"quantity": floor(amount * (10 ** self._symbols[symbol].step)) / (10 ** self._symbols[symbol].step),
			"price": round(price, self._symbols[symbol].step),
		}
		resp = self._http_request("order", data, auth=True)
		if not resp or "code" in resp or resp["status"] not in ["NEW", "PARTIALLY_FILLED", "FILLED"]:
			return None
		order = Order(
			resp["orderId"], side, symbol, price,
			float(resp["origQty"]), float(resp["executedQty"]),
			Binance.ORDER_STATES[resp["status"]]
		)
		self._orders[order.id] = order
		return order

	def cancel_order(self, order_id):
		if order_id not in self._orders:
			return False
		data = {
			"symbol": self._orders[order_id].symbol,
			"orderId": self._orders[order_id].id,
		}
		resp = self._http_request("order", data, method="DELETE", auth=True)
		if not resp or "code" in resp:
			return False
		self._orders[order_id].update(
			Binance.ORDER_STATES[resp["status"]],
			float(resp["executedQty"])
		)
		return True

	def check_order(self, order_id):
		if order_id not in self._orders:
			return False
		data = {
			"symbol": self._orders[order_id].symbol,
			"orderId": self._orders[order_id].id
		}
		resp = self._http_request("order", data, method="GET", auth=True)
		if not resp or "code" in resp:
			return False
		self._orders[order_id].update(Binance.ORDER_STATES[resp["status"]], float(resp["executedQty"]))
		return True

	def get_graph_interval(self, symbol, interval, length=1000, raw=False, counter=0):
		try:
			data = self._http_request(
				"klines?&symbol=%s&interval=%s&limit=%s" % (symbol, interval, length),
				method="GET",
			)
			if not data:
				raise Exception
		except Exception:
			print("Failed to load %s %s graph on %s. Retry in 1 second." % (symbol, interval, self.name))
			if self.retry_limit and counter < self.retry_limit:
				sleep(1)
				return self.get_graph_interval(symbol, interval, length, counter=counter + 1)
			else:
				return []
		if raw:
			return data
		graph = []
		for c in data:
			graph.append({
				"open_time": c[0],
				"close_time": c[6],
				"open_ask": float(c[1]),
				"open_bid": float(c[1]),
				"close_ask": float(c[4]),
				"close_bid": float(c[4]),
				"high_ask": float(c[2]),
				"high_bid": float(c[2]),
				"low_ask": float(c[3]),
				"low_bid": float(c[3]),
				"volume": float(c[5])
			})
		self._symbols[symbol].set_graph_interval(interval, graph)
		return graph

	async def subscribe(self, callback, raw=False, counter=0):
		streams = ""
		for symbol in self._symbols:
			streams += "/" if len(streams) else ""
			streams += "%s@kline_1m" % (symbol.lower())
		uri = "%s?streams=%s" % (Binance.__stream, streams)
		while True:
			try:
				ws = await connect(uri)
				counter = 0
				print("Stream connected - %s" % uri)
				while True:
					if self.__exit_stream:
						self.__exit_stream = False
						return
					txt = await ws.recv()
					if raw:
						await callback(txt)
					else:
						await self._process(txt, callback)
			except Exception as e:
				print("Exception from subscribe: %s" % e)
				counter += 1
				if self.retry_limit and counter >= self.retry_limit:
					return
				else:
					print("Unable to connect stream at uri: %s (next attempt in 1s)" % uri)
					sleep(1)

	def exit_stream(self):
		self.__exit_stream = True

	async def _process(self, txt, callback):
		data = loads(txt.encode())["data"]
		symbol = self._symbols[data["s"]]
		time = data["E"]
		data = data["k"]
		candle = {
			"time": time,
			"open_time": data["t"],
			"close_time": data["T"],
			"open_ask": float(data["o"]),
			"open_bid": float(data["o"]),
			"close_ask": float(data["c"]),
			"close_bid": float(data["c"]),
			"high_ask": float(data["h"]),
			"high_bid": float(data["h"]),
			"low_ask": float(data["l"]),
			"low_bid": float(data["l"]),
			"volume": float(data["v"]),
			"closed": data["x"]
		}
		symbol.update(candle)
		await callback(symbol)

	def _http_request(self, action="", data=None, method="POST", auth=False):
		params = ""
		url = self.__endpoint + action
		if auth:
			data = data or {}
			data["recvWindow"] = 60000
			data["timestamp"] = int(time() * 1000)
		if data:
			params = "?"
			for key in data:
				params += "%s=%s&" % (key, data[key])
			if auth:
				if "SECRET_KEY" not in self.__credentials or "API_KEY" not in self.__credentials:
					return None
				signature = new(
					self.__credentials["SECRET_KEY"],
					params[1:-1].encode(),
					sha256
				).hexdigest()
				params += "signature=%s" % signature
		try:
			req = Request(url + params, method=method)
			if auth:
				req.add_header("X-MBX-APIKEY", self.__credentials["API_KEY"])
			with urlopen(req) as response:
				return loads(response.read())
		except Exception as e:
			print("Unable to connect Binance REST API at URL: %s" % (url + params))
			print(e)
			return None
