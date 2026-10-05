from yaml import serialize
from enum import StrEnum
from string.templatelib import Template
from typing import Optional, Any

import serde

from ..base import Duration, strenum_field
from ..base import  strenum_list_field

class Proc(StrEnum):
	Wave = "wave"
	Knockback = "knockback"
	Freeze = "freeze"
	Slow = "slow"
	Weaken = "weaken"
	Surge = "surge"
	Blast = "blast"
	Curse = "curse"
	Warp = "warp"
	Bosswave = "boss_wave"
	Toxic = "toxic"
	Delay = "delay"

@serde.serde(transparent=True)
class Immunity:
	to: Proc = strenum_field(Proc)

	def __str__(self):
		return self.to.value

@serde.serde
class Resist:
	by: int
	to: Proc = strenum_field(Proc)

	def __str__(self):
		return f"resists {self.to} by {self.by}%"


@serde.serde
class CounterSurge:
	def __str__(self):
		return "has counter surge"


@serde.serde
class WaveBlock:
	def __str__(self):
		return "has wave block"


@serde.serde
class Barrier:
	health: int

	def __str__(self):
		return f"barrier with {self.health} HP"


@serde.serde
class Survive:
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to survive a lethal attack"


@serde.serde
class Shield:
	health: int
	regeneration: int

	def __str__(self):
		return f"has an aku shield with {self.health} HP that regenerates by {self.regeneration}%"


@serde.serde
class Revive:
	count: int
	delay: int
	health: int

	def __str__(self):
		return f"revives to {self.health}% after {self.delay}f up to {self.count if self.count > 0 else "infinite"} times"


@serde.serde
class Strengthen:
	health: int
	by: int

	def __add__(self, other) -> 'Strengthen':
		return Strengthen(self.health, self.by + other.mult)

	def __floordiv__(self, other) -> 'Strengthen':
		return Strengthen(self.health, self.by // other)

	def __str__(self):
		return f"strengthens by +{self.by}% at {self.health}% HP"


@serde.serde
class BehemothDodge:
	chance: int
	duration: Duration

	def text(self) -> Template:
		return t"{self.chance}% chance to dodge behemoth attacks for {self.duration}"


@serde.serde
class Metal:
	def __str__(self):
		return "metal"


@serde.serde(skip_if_default=True)
class BaseDefensives:
	counter_surge: Optional[CounterSurge] = None
	wave_block: Optional[WaveBlock] = None
	barrier: Optional[Barrier] = None
	survive: Optional[Survive] = None
	shield: Optional[Shield] = None
	revive: Optional[Revive] = None
	strengthen: Optional[Strengthen] = None
	behemoth_dodge: Optional[BehemothDodge] = None
	metal: Optional[Metal] = None

	@property
	def items(self) -> list[Any]:
		return [x for x in (self.counter_surge, self.wave_block, self.barrier, self.survive, self.shield, self.revive, self.strengthen, self.behemoth_dodge, self.metal) if x is not None]


# --- #

@serde.serde
class Suicide:
	def __str__(self):
		return "suicides on hit"


@serde.serde
class ZombieKiller:
	def __str__(self):
		return "zombie killer"


@serde.serde
class SoulStrike:
	def __str__(self):
		return "soul strike"


@serde.serde
class DoubleBounty:
	def __str__(self):
		return "double bounty"


@serde.serde
class BaseDestroyer:
	def __str__(self):
		return "base destroyer"


@serde.serde
class BarrierBreak:
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to break enemy barrier"


@serde.serde
class ShieldBreak:
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to break Aku shield"


@serde.serde
class Critical:
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to deal a critical hit"


@serde.serde
class SavageBlow:
	chance: int
	amount: float

	def __str__(self):
		return f"{self.chance}% chance to deal a savage blow which does +{self.amount:.0f}% damage"


@serde.serde
class Burrow:
	count: int
	distance: int

	def __str__(self):
		return f"burrows by {self.distance // 4} up to {self.count} time/s"


@serde.serde
class Conjure:
	spirit_id: int

	def __str__(self):
		return f"conjures spirit ID {self.spirit_id}"


@serde.serde
class MetalKiller:
	damage: int

	def __str__(self):
		return f"deals metal killer damage equal to {self.damage}% of enemy's current HP"


@serde.serde(skip_if_default=True, skip_if_none=True)
class BaseOffensives:
	suicide: Optional[Suicide] = None
	zombie_killer: Optional[ZombieKiller] = None
	soul_strike: Optional[SoulStrike] = None
	double_bounty: Optional[DoubleBounty] = None
	base_destroyer: Optional[BaseDestroyer] = None
	barrier_break: Optional[BarrierBreak] = None
	shield_break: Optional[ShieldBreak] = None
	critical: Optional[Critical] = None
	savage_blow: Optional[SavageBlow] = None
	burrow: Optional[Burrow] = None
	conjure: Optional[Conjure] = None
	metal_killer: Optional[MetalKiller] = None

	@property
	def items(self) -> list[Any]:
		return [x for x in (self.suicide, self.zombie_killer, self.soul_strike, self.double_bounty, self.base_destroyer, self.barrier_break, self.shield_break, self.critical, self.savage_blow, self.burrow, self.conjure, self.metal_killer) if x is not None]


@serde.serde(skip_if_default=True)
class Passives:
	defensives: BaseDefensives = serde.field(flatten=True)
	offensives: BaseOffensives = serde.field(flatten=True)
	immunities: list[Immunity] = serde.field(default_factory=list)
	resistances: list[Resist] = serde.field(default_factory=list)
