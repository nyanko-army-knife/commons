import enum

from commons.models.base import Model


class ComboSize(Model):
	id_: int = 0
	name: str = ""


class ComboEffect(Model):
	id_: int = 0
	name: str = ""


class ComboCondition(enum.IntEnum):
	UNUSED = -1
	EOC_1 = 1
	EOC_2 = 2
	EOC_3 = 3
	ITF_1 = 4
	ITF_2 = 5
	ITF_3 = 6
	COTC_1 = 7
	COTC_2 = 8
	COTC_3 = 9
	UR_2700 = 10001
	UR_1450 = 10002
	UR_2150 = 10003


class Combo(Model):
	id_: int
	cats: list[tuple[int, int]]
	name: str
	size: ComboSize
	effect: ComboEffect
	condition: ComboCondition

	@property
	def used(self):
		return self.condition != -1
