from copy import deepcopy
from typing import Optional, Self

from commons.models.base import Model


def damage_scale(dmg: int, level_mult: float, treasure_mult: float) -> int:
	_base_dmg = dmg
	dmg = round(dmg * level_mult)
	dmg += int(dmg * treasure_mult)
	return dmg


class Hit(Model):
	use_ability: bool = False
	separate_range: bool = False
	damage: int = 0
	range_start: int = 0
	range_width: int = 0
	foreswing: int = 0

	# replaces foreswing with delay
	def after(self, other: Self) -> Self:
		toret = deepcopy(self)
		toret.foreswing -= other.foreswing
		return toret

	def __str__(self):
		out = f'{self.foreswing}f: '
		if self.use_ability:
			out += f"**__{self.damage}__**"
		else:
			out += f"{self.damage}"

		if self.separate_range:
			out += f' [{self.range_start}~{self.range_start + self.range_width}]'
		return out


class AttackBreakup(Model):
	hit_0: Hit
	hit_1: Optional[Hit] = None
	hit_2: Optional[Hit] = None
	backswing: int = -1
	cooldown: int = -1

	def __str__(self):
		out = ""
		out += f" ↑{self.hit_0}\n"
		if self.hit_1:
			out += f" ↑{self.hit_1.after(self.hit_0)}\n"
			if self.hit_2: out += f" ↑{self.hit_2.after(self.hit_1)}\n"
		out += f' ↓{self.backswing}f / ⏲{self.tba}f\n'
		return out

	def scale(self, level_mult: float, treasure_mult: float = 0) -> Self:
		toret = deepcopy(self)
		if toret.hit_0: toret.hit_0.damage = damage_scale(toret.hit_0.damage, level_mult, treasure_mult)
		if toret.hit_1: toret.hit_1.damage = damage_scale(toret.hit_1.damage, level_mult, treasure_mult)
		if toret.hit_2: toret.hit_2.damage = damage_scale(toret.hit_2.damage, level_mult, treasure_mult)
		return toret

	def hits(self) -> list[Hit]:
		return [hit for hit in (self.hit_0, self.hit_1, self.hit_2) if hit is not None]

	@property
	def fullswing(self) -> int:
		return self.hits()[-1].foreswing + self.backswing

	@property
	def cd_effective(self) -> int:
		return self.hits()[-1].foreswing + max(self.backswing, self.cooldown - 1)

	@property
	def tba(self) -> int:
		return self.cd_effective - self.fullswing
