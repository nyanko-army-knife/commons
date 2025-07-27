# abilities that extend the attack's effect
from typing import Union

from commons.models.abilities.base import Ability

type Extension = Union[Wave, Surge, DeathSurge, Blast]


class BaseExtension(Ability):
	pass


class Wave(BaseExtension):
	chance: int = 0
	level: int = 0
	mini: bool = False

	def __str__(self):
		return f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}wave"


class Surge(BaseExtension):
	chance: int = 0
	level: int = 0
	range_start: int = 0
	range_width: int = 0
	mini: bool = False

	def __str__(self):
		if self.range_width > 0:
			return (f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}"
							f"surge between {self.range_start // 4:.0f}~{(self.range_start + self.range_width) // 4:.0f} range")
		else:
			return (f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}"
							f"surge at {self.range_start // 4:.0f} range")


class DeathSurge(BaseExtension):
	pass


class Blast(BaseExtension):
	chance: int = 0
	range_start: int = 0
	range_width: int = 0

	def __str__(self):
		if self.range_width > 0:
			return (f"{self.chance}% chance to create a blast between "
							f"{self.range_start // 4}~{(self.range_start + self.range_width) // 4} range")
		else:
			return f"{self.chance}% chance to create a blast at {self.range_start // 4} range"
