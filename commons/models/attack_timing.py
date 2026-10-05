from copy import deepcopy
from string.templatelib import Template
from typing import Optional, Self

import serde

from commons.models.base import Duration


def damage_scale(dmg: int, level_mult: float, treasure_mult: float) -> int:
	_base_dmg = dmg
	dmg = round(dmg * level_mult)
	dmg += int(dmg * treasure_mult)
	return dmg


@serde.serde(skip_if_default=True)
class Hit:
	use_ability: bool = False
	separate_range: Optional[tuple[int, int]] = None
	damage: int = 0
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
			range_start, range_width = self.separate_range
			out += t' [{range_start}~{range_start + range_width}]'
		return out


@serde.serde(skip_if_default=True)
class AttackBreakup:
	hit_0: Hit = serde.field(default_factory=Hit)
	hit_1: Optional[Hit] = None
	hit_2: Optional[Hit] = None
	backswing: Duration = Duration(-1)
	cooldown: Duration = Duration(-1)

	def text(self) -> Template:
		toprint = deepcopy(self)
		# don't print hit0-range for non-seperate-range units
		if toprint.hit_1 and not toprint.hit_1.separate_range:
			toprint.hit_0.separate_range = None

		out = t""
		out += t" ↑{toprint.hit_0}\n"
		if toprint.hit_1:
			out += t" ↑{toprint.hit_1.after(toprint.hit_0)}\n"
			if toprint.hit_2: out += t" ↑{toprint.hit_2.after(toprint.hit_1)}\n"
		out += t' ↓{toprint.backswing} / ⏲{toprint.tba}\n'
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
