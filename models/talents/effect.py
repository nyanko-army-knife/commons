from dataclasses import dataclass

from commons.models.base import Model


@dataclass
class Effect[T](Model):
	_klass = 'effect'

	level_1: T
	level_max: T

	def apply_level(self, level: int, max_level: int) -> T:
		assert max_level >= level > 0
		if level == 1: return self.level_1

		diff = (self.level_max - self.level_1) / (max_level - 1)
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
