# abilities that extend the attack's effect

from dataclasses import dataclass

from commons.models.abilities.base import Ability


@dataclass
class Extension(Ability):
	pass


@dataclass
class Wave(Extension):
	_klass = "wave"

	chance: int = 0
	level: int = 0
	mini: bool = False

	def __str__(self):
		return f"{self.chance}% chance to create a level {self.level} {'mini' if self.mini else ''}wave"


@dataclass
class Surge(Extension):
	_klass = "surge"

	chance: int = 0
	level: int = 0
	range_start: int = 0
	range_width: int = 0
	mini: bool = False

	def __str__(self):
		if self.range_width > 0:
			return f"{self.chance}% chance to create a {'mini' if self.mini else ''}surge between {self.range_start // 4}~{(self.range_start + self.range_width) // 4} range"
		else:
			return f"{self.chance}% chance to create a {'mini' if self.mini else ''}surge at {self.range_start // 4} range"


@dataclass
class DeathSurge(Surge):
	_klass = "death_surge"


@dataclass
class Blast(Extension):
	_klass = "blast"

	chance: int = 0
	range_start: int = 0
	range_width: int = 0

	def __str__(self):
		if self.range_width > 0:
			return f"{self.chance}% chance to create a blast between {self.range_start // 4}~{(self.range_start + self.range_width) // 4} range"
		else:
			return f"{self.chance}% chance to create a blast at {self.range_start // 4} range"
