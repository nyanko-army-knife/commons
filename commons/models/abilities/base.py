from copy import deepcopy

import msgspec

from commons.models.base import Model


class Ability(Model):
	def __sub__(self, other):
		out = deepcopy(self)
		for field in msgspec.inspect.type_info(type(self)).fields:
			if isinstance(field.type, msgspec.inspect.IntType):
				out.__setattr__(field.name, self.__getattribute__(field.name) - other.__getattribute__(field.name))
		return out

	def __add__(self, other):
		out = deepcopy(self)
		for field in msgspec.inspect.type_info(type(self)).fields:
			if isinstance(field.type, msgspec.inspect.IntType):
				out.__setattr__(field.name, self.__getattribute__(field.name) + other.__getattribute__(field.name))
		return out

	def __floordiv__(self, other: int):
		out = deepcopy(self)
		for field in msgspec.inspect.type_info(type(self)).fields:
			if isinstance(field.type, msgspec.inspect.IntType):
				out.__setattr__(field.name, self.__getattribute__(field.name) // other)
		return out
