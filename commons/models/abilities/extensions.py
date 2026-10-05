# abilities that extend the attack's effect
import serde
from typing import Union, Optional, Any

from commons.models.abilities.base import Ability



@serde.serde
class Wave:
	chance: int = 0
	level: int = 0
	mini: bool = False

	def __str__(self):
		return f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}wave"


@serde.serde
class Surge:
	chance: int = 0
	level: int = 0
	range: tuple[int, int] = (0, 0)
	mini: bool = False

	def __str__(self):
		if self.range[1] > 0:
			return (f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}"
							f"surge between {self.range[0] // 4:.0f}~{(self.range[0] + self.range[1]) // 4:.0f} range")
		else:
			return (f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}"
							f"surge at {self.range[0] // 4:.0f} range")


@serde.serde
class DeathSurge:
	pass


@serde.serde
class Blast:
	chance: int = 0
	range_start: int = 0
	range_width: int = 0

	def __str__(self):
		if self.range_width > 0:
			return (f"{self.chance}% chance to create a blast between "
							f"{self.range_start // 4}~{(self.range_start + self.range_width) // 4} range")
		else:
			return f"{self.chance}% chance to create a blast at {self.range_start // 4} range"

@serde.serde(skip_if_default=True, skip_if_none=True)
class Extension:
	wave: Optional[Wave] = None
	surge: Optional[Surge] = None
	death_surge: Optional[DeathSurge] = None
	blast: Optional[Blast] = None

	@property
	def items(self) -> list[Any]:
		return [x for x in (self.wave, self.surge, self.death_surge, self.blast) if x is not None]
