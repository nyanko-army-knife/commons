import dataclasses
from copy import deepcopy
from dataclasses import dataclass

from commons.models.base import Model


@dataclass
class Ability(Model):
	def __sub__(self, other):
		out = deepcopy(self)
		for field in dataclasses.fields(self):
			if field.type is int:
				out.__setattr__(field.name, self.__getattribute__(field.name) - other.__getattribute__(field.name))
		return out

	def __add__(self, other):
		out = deepcopy(self)
		for field in dataclasses.fields(self):
			if field.type is int:
				out.__setattr__(field.name, self.__getattribute__(field.name) + other.__getattribute__(field.name))
		return out

	def __floordiv__(self, other: int):
		out = deepcopy(self)
		for field in dataclasses.fields(self):
			if field.type is int:
				out.__setattr__(field.name, self.__getattribute__(field.name)//other)
		return out
