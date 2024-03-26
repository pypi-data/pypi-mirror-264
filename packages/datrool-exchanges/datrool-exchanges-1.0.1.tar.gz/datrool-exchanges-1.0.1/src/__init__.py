# -*- coding: utf-8 -*-
from .binance import Binance
__version__ = "1.0.1"

wrapper_list = {
	"binance": Binance
}


def load_exchange(name):
	if name in wrapper_list:
		return wrapper_list[name]
	else:
		raise NotImplementedError("no exchange named `%s`" % name)
