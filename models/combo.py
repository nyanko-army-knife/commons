import enum
from dataclasses import dataclass, field

from commons.models.base import Model


@dataclass
class Combo(Model):
	_klass = "combo"

	id_: int = 0
	cats: list[tuple[int, int]] = field(default_factory=list)
	name: str = ""
	size: "ComboSize" = None
	effect: "ComboEffect" = None
	condition: "ComboCondition" = None

	@property
	def used(self):
		return self.condition != -1


@dataclass
class ComboSize(Model):
	_klass = "combo_size"

	id_: int = 0
	name: str = ""


@dataclass
class ComboEffect(Model):
	_klass = "combo_effect"
	id_: int = 0
	name: str = ""


class ComboCondition(int, enum.Enum):
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
