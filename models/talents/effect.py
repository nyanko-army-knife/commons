from typing import TYPE_CHECKING, Optional

from commons.models.base import Model

from ... import c
from .. import ActiveAbility, Extension
from ..abilities import (
	BaseActiveAbility,
	BaseDefensive,
	BaseExtension,
	BaseOffensive,
	BaseStatMod,
	Defensive,
	Immunity,
	Offensive,
	Resist,
	StatMod,
)

if TYPE_CHECKING:
	from ..unit import Form

type EffectAbility = Offensive | Defensive | ActiveAbility | StatMod | Extension | Immunity | Resist


class Effect[T: EffectAbility](Model):
	level_1: T
	level_max: Optional[T]

	def get_level(self, level: int, max_level: int) -> T:
		if not (max_level >= level > 0): level = max_level
		if level == 1 or self.level_max is None: return self.level_1

		diff = (self.level_max - self.level_1) // (max_level - 1)
		out = self.level_1
		for i in range(level - 1):
			out += diff
		return out


class Talent(Model):
	effects: list[Effect[EffectAbility]]
	np_curve: list[int]
	name: str
	text: str
	max_level: int = 10
	is_ultra: bool = False

	def apply_level_to(self, level: int, cat: 'Form') -> 'Form':
		def upsert(elems: list, new_elem):
			for i, elem in enumerate(elems):
				if type(elem) is type(new_elem):
					elems[i] = elem + new_elem
					return
			elems.append(new_elem)

		for effect in self.effects:
			e = effect.get_level(level, self.max_level)
			match e:
				case BaseDefensive():
					upsert(cat.passives.defensives, e)
				case BaseOffensive():
					upsert(cat.passives.offensives, e)
				case BaseStatMod():
					e.apply(cat)
				case BaseActiveAbility():
					upsert(cat.abilities, e)
				case BaseExtension():
					upsert(cat.extensions, e)
				case Immunity():
					cat.passives.immunities.append(e)
				case Resist():
					cat.passives.resists.append(e)
				case _:
					c.logger.error(f"unknown effect {e}")
		return cat
