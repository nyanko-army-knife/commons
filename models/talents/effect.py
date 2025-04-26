from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Optional

from commons.models.base import Model
from extractors import c
from .. import ActiveAbility, Extension
from ..abilities import Defensive, Offensive, StatMod, Immunity, Resist

if TYPE_CHECKING:
	from ..unit import Form

T = TypeVar('T')


@dataclass
class Effect[T](Model):
	_klass = 'effect'

	level_1: T
	level_max: Optional[T]

	def get_level(self, level: int, max_level: int) -> T:
		if not (max_level >= level > 0): level = max_level
		if level == 1: return self.level_1

		diff = (self.level_max - self.level_1) // (max_level - 1)
		out = self.level_1
		for i in range(level - 1):
			out += diff
		return out


@dataclass
class Talent[T](Model):
	_klass = 'talent'

	effects: list[Effect[T]]
	np_curve: list[int]
	name: str
	text: str
	max_level: int = 10
	is_ultra: bool = False

	def apply_level_to(self, level: int, cat: 'Form') -> 'Form':
		def upsert(elems: list, new_elem):
			for i, elem in enumerate(elems):
				if elem.klass() == new_elem.klass():
					elems[i] = elem + new_elem
					return
			elems.append(new_elem)

		for effect in self.effects:
			e = effect.get_level(level, self.max_level)
			match e:
				case Defensive():
					upsert(cat.passives.defensives, e)
				case Offensive():
					upsert(cat.passives.offensives, e)
				case StatMod():
					e.apply(cat)
				case ActiveAbility():
					upsert(cat.abilities, e)
				case Extension():
					upsert(cat.extensions, e)
				case Immunity():
					cat.passives.immunities.append(e)
				case Resist():
					cat.passives.resists.append(e)
				case _:
					c.logger.error("unknown effect", e)
		return cat
