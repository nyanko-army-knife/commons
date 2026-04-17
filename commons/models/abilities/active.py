from string.templatelib import Template
from typing import Union

from .base import Ability
from ..base import Duration

type ActiveAbility = Union[Slow, Freeze, Knockback, Weaken, Warp, Curse, Toxic, Dodge, TargetOnly]


class BaseActiveAbility(Ability):
	pass


class Slow(BaseActiveAbility):
	chance: int = 0
	duration: Duration = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to slow for {self.duration}"


class Freeze(BaseActiveAbility):
	chance: int = 0
	duration: Duration = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to freeze for {self.duration}"


class Knockback(BaseActiveAbility):
	chance: int = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to knockback"


class Weaken(BaseActiveAbility):
	chance: int = 0
	duration: Duration = 0
	amount: int = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to weaken to {self.amount}% for {self.duration}"


class Warp(BaseActiveAbility):
	chance: int = 0
	duration: Duration = 0
	dist_min: int = 0
	dist_max: int = 0

	def text(self) -> Template:
		if self.dist_max != self.dist_min:
			return t"{self.chance}% chance to warp for {self.duration}f over {self.dist_min}~{self.dist_max}"
		else:
			return t"{self.chance}% chance to warp for {self.duration}f over {self.dist_min}"


class Curse(BaseActiveAbility):
	chance: int = 0
	duration: Duration = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to curse for {self.duration}"


class Toxic(BaseActiveAbility):
	chance: int = 0
	amount: int = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to inflict {self.amount}% toxic damage"


class Dodge(BaseActiveAbility):
	chance: int = 0
	duration: Duration = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to dodge for {self.duration}"


class TargetOnly(BaseActiveAbility):
	def __str__(self):
		return "only attacks its target traits"
