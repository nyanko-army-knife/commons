from dataclasses import dataclass

from commons.models.abilities.base import Ability


class ActiveAbility(Ability):
	pass


@dataclass
class Slow(ActiveAbility):
	_klass = "slow"

	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to slow for {self.duration}f"


@dataclass
class Freeze(ActiveAbility):
	_klass = "freeze"

	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to freeze for {self.duration}f"


@dataclass
class Knockback(ActiveAbility):
	_klass = "knockback"

	chance: int = 0

	def __str__(self):
		return f"{self.chance}% chance to knockback"


@dataclass
class Weaken(ActiveAbility):
	_klass = "weaken"

	chance: int = 0
	duration: int = 0
	amount: int = 0

	def __str__(self):
		return f"{self.chance}% chance to weaken to {self.amount}% for {self.duration}f"


@dataclass
class Warp(ActiveAbility):
	_klass = "warp"

	chance: int = 0
	duration: int = 0
	dist_min: int = 0
	dist_max: int = 0

	def __str__(self):
		if self.dist_max != self.dist_min:
			return f"{self.chance}% chance to warp for {self.duration}f over {self.dist_min}~{self.dist_max}"
		else:
			return f"{self.chance}% chance to warp for {self.duration}f over {self.dist_min}"


@dataclass
class Curse(ActiveAbility):
	_klass = "curse"

	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to curse for {self.duration}f"


@dataclass
class Toxic(ActiveAbility):
	_klass = "toxic"

	chance: int = 0
	amount: int = 0

	def __str__(self):
		return f"{self.chance}% chance to inflict {self.amount}% toxic damage"


@dataclass
class Dodge(ActiveAbility):
	_klass = "dodge"

	chance: int = 0
	duration: int = 0

	def __str__(self):
		return f"{self.chance}% chance to dodge for {self.duration}f"


@dataclass
class TargetOnly(ActiveAbility):
	_klass = "target_only"

	def __str__(self):
		return "only attacks its target traits"
