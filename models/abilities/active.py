from typing import Union

from .base import Ability

type ActiveAbility = Union[Slow, Freeze, Knockback, Weaken, Warp, Curse, Toxic, Dodge, TargetOnly]


class BaseActiveAbility(Ability):
	pass


class Slow(BaseActiveAbility):
	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to slow for {self.duration}f"


class Freeze(BaseActiveAbility):
	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to freeze for {self.duration}f"


class Knockback(BaseActiveAbility):
	chance: int = 0

	def __str__(self):
		return f"{self.chance}% chance to knockback"


class Weaken(BaseActiveAbility):
	chance: int = 0
	duration: int = 0
	amount: int = 0

	def __str__(self):
		return f"{self.chance}% chance to weaken to {self.amount}% for {self.duration}f"


class Warp(BaseActiveAbility):
	chance: int = 0
	duration: int = 0
	dist_min: int = 0
	dist_max: int = 0

	def __str__(self):
		if self.dist_max != self.dist_min:
			return f"{self.chance}% chance to warp for {self.duration}f over {self.dist_min}~{self.dist_max}"
		else:
			return f"{self.chance}% chance to warp for {self.duration}f over {self.dist_min}"


class Curse(BaseActiveAbility):
	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to curse for {self.duration}f"


class Toxic(BaseActiveAbility):
	chance: int = 0
	amount: int = 0

	def __str__(self):
		return f"{self.chance}% chance to inflict {self.amount}% toxic damage"


class Dodge(BaseActiveAbility):
	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to dodge for {self.duration}f"


class TargetOnly(BaseActiveAbility):
	def __str__(self):
		return "only attacks its target traits"
