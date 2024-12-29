import enum
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Combo:
	_klass="combo"

	id: int = 0
	cats: list[tuple[int, int]] = field(default_factory=list)
	name: str = ""
	size: "ComboSize" = None
	effect: "ComboEffect" = None
	condition: "ComboCondition" = None

	@property
	def used(self):
		return self.condition != -1



@dataclass
class ComboSize:
	_klass="combo_size"

	id: int = 0
	name: str = ""

@dataclass
class ComboEffect:
	_klass="combo_effect"
	id: int = 0
	name: str = ""

class ComboCondition(enum.Enum):
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
