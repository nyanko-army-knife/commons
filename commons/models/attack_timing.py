from copy import deepcopy
from string.templatelib import Template
from typing import Optional, Self

from msgspec import field

from commons.models.base import Model, Duration


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
	foreswing: Duration = Duration(0)

	# replaces foreswing with delay
	def after(self, other: Self) -> Self:
		toret = deepcopy(self)
		toret.foreswing = Duration(toret.foreswing - other.foreswing)
		return toret

	def text(self) -> Template:
		out = t'{self.foreswing}: '
		if self.use_ability:
			out += t"**__{self.damage}__**"
		else:
			out += t"{self.damage}"

		if self.separate_range:
			out += t' [{self.range_start}~{self.range_start + self.range_width}]'
		return out


class AttackBreakup(Model):
	hit_0: Hit = field(default_factory=Hit)
	hit_1: Optional[Hit] = None
	hit_2: Optional[Hit] = None
	backswing: Duration = Duration(-1)
	cooldown: Duration = Duration(-1)

	def text(self) -> Template:
		out = t""
		out += t" ↑{self.hit_0}\n"
		if self.hit_1:
			out += t" ↑{self.hit_1.after(self.hit_0)}\n"
			if self.hit_2: out += t" ↑{self.hit_2.after(self.hit_1)}\n"
		out += t' ↓{self.backswing} / ⏲{self.tba}\n'
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
	def fullswing(self) -> Duration:
		return Duration(self.hits()[-1].foreswing + self.backswing)

	@property
	def cd_effective(self) -> Duration:
		return Duration(self.hits()[-1].foreswing + max(self.backswing, self.cooldown - Duration(1)))

	@property
	def tba(self) -> Duration:
		return Duration(self.cd_effective - self.fullswing)
