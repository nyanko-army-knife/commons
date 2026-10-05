import serde
from string.templatelib import Template
from typing import Union, Optional, Any

from .base import Ability
from ..base import Duration


@serde.serde
class Slow:
	chance: int = 0
	duration: Duration = Duration(0)

	def text(self) -> Template:
		return t"{self.chance}% chance to slow for {self.duration}"

@serde.serde
class Freeze:
	chance: int = 0
	duration: Duration = Duration(0)

	def text(self) -> Template:
		return t"{self.chance}% chance to freeze for {self.duration}"

@serde.serde
class Knockback:
	chance: int = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to knockback"

@serde.serde
class Weaken:
	chance: int = 0
	duration: Duration = Duration(0)
	to: int = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to weaken to {self.to}% for {self.duration}"

@serde.serde
class Warp:
	chance: int = 0
	duration: Duration = Duration(0)
	distance: tuple[int, int] = (0, 0)

	def text(self) -> Template:
		if self.distance[0] != self.distance[1]:
			return t"{self.chance}% chance to warp for {self.duration} over {self.distance[0] // 4}~{self.distance[1] // 4}"
		else:
			return t"{self.chance}% chance to warp for {self.duration} over {self.distance[0] // 4}"

@serde.serde
class Curse:
	chance: int = 0
	duration: Duration = Duration(0)

	def text(self) -> Template:
		return t"{self.chance}% chance to curse for {self.duration}"

@serde.serde
class Toxic:
	chance: int = 0
	amount: int = 0

	def text(self) -> Template:
		return t"{self.chance}% chance to inflict {self.amount}% toxic damage"

@serde.serde
class Dodge:
	chance: int = 0
	duration: Duration = Duration(0)

	def text(self) -> Template:
		return t"{self.chance}% chance to dodge for {self.duration}"

@serde.serde
class TargetOnly:
	def __str__(self):
		return "only attacks its target traits"

@serde.serde
class ActiveAbility:
	slow: Optional[Slow]
	freeze: Optional[Freeze]
	knockback: Optional[Knockback]
	weaken: Optional[Weaken]
	warp: Optional[Warp]
	curse: Optional[Curse]
	toxic: Optional[Toxic]
	dodge: Optional[Dodge]
	target_only: Optional[TargetOnly]

	@property
	def items(self) -> list[Any]:
		return [x for x in (self.slow, self.freeze, self.knockback, self.weaken, self.warp, self.curse, self.toxic, self.dodge, self.target_only) if x is not None]
