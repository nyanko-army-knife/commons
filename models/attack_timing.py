from copy import deepcopy
from dataclasses import dataclass

from commons.models.base import Model


def damage_scale(dmg: int, level_mult: float, treasure_mult: float) -> int:
	base_dmg = dmg
	dmg = round(dmg * level_mult)
	dmg += int(dmg * treasure_mult)
	return dmg


@dataclass
class Hit(Model):
	_klass = "hit"

	use_ability: bool = False
	separate_range: bool = False
	damage: int = 0
	range_start: int = 0
	range_width: int = 0
	foreswing: int = 0

	def __str__(self):
		out = f'{self.foreswing}f: {self.damage}'
		if self.separate_range:
			out += f' [{self.range_start}~{self.range_start + self.range_width}]'
		if self.use_ability:
			out = f"_{out}_"
		return out


@dataclass
class AttackBreakup(Model):
	_klass = "attack_breakup"

	hit_0: Hit = None
	hit_1: Hit = None
	hit_2: Hit = None
	backswing: int = 0
	cooldown: int = 0

	def __str__(self):
		out = ""
		for hit in self.hit_0, self.hit_1, self.hit_2:
			if hit is not None:
				out += str(hit) + '\n'
		out += f'backswing: {self.backswing}f, TBA: {self.tba}f\n'
		return out

	def scale(self, level_mult: float, treasure_mult: float) -> 'AttackBreakup':
		toret = deepcopy(self)
		if toret.hit_0 is not None: toret.hit_0.damage = damage_scale(toret.hit_0.damage, level_mult, treasure_mult)
		if toret.hit_1 is not None: toret.hit_1.damage = damage_scale(toret.hit_1.damage, level_mult, treasure_mult)
		if toret.hit_2 is not None: toret.hit_2.damage = damage_scale(toret.hit_2.damage, level_mult, treasure_mult)
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
