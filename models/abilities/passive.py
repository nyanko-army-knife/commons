from enum import StrEnum
from typing import Union

from msgspec import field

from ..abilities.base import Ability
from ..base import Model


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
	BossWave = "boss_wave"
	Toxic = "toxic"


class Immunity(Ability):
	to: Proc

	def __str__(self):
		return f"immune to {self.to}"


class Resist(Ability):
	to: Proc
	amt: int

	def __str__(self):
		return f"resists {self.to} by {self.amt}%"


type Defensive = Union[CounterSurge, WaveBlock, Barrier, Survive, Shield, Revive, Strengthen, BehemothDodge, Metal]


class BaseDefensive(Ability):
	pass


class CounterSurge(BaseDefensive):
	def __str__(self):
		return "has counter surge"


class WaveBlock(BaseDefensive):
	def __str__(self):
		return "has wave block"


class Barrier(BaseDefensive):
	health: int

	def __str__(self):
		return f"barrier with {self.health} HP"


class Survive(BaseDefensive):
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to survive a lethal attack"


class Shield(BaseDefensive):
	health: int
	regen: int

	def __str__(self):
		return f"has an aku shield with {self.health} HP that regenerates by {self.regen}%"


class Revive(BaseDefensive):
	count: int
	delay: int
	health: int

	def __str__(self):
		return f"revives to {self.health}% after {self.delay}f up to {self.count} times"


class Strengthen(BaseDefensive):
	health: int
	mult: int

	def __str__(self):
		return f"strengthens by +{self.mult}% at {self.health}% HP"


class BehemothDodge(BaseDefensive):
	chance: int
	duration: int

	def __str__(self):
		return f"{self.chance}% chance to dodge behemoth attacks for {self.duration}f"


class Metal(BaseDefensive):
	def __str__(self):
		return "metal"


# --- #

type Offensive = Union[Suicide, ZombieKiller, SoulStrike, DoubleBounty, BaseDestroyer, BarrierBreak, ShieldBreak,
Critical, SavageBlow, Burrow, Conjure, MetalKiller]


class BaseOffensive(Ability):
	pass


class Suicide(BaseOffensive):
	def __str__(self):
		return "suicides on hit"


class ZombieKiller(BaseOffensive):
	def __str__(self):
		return "zombie killer"


class SoulStrike(BaseOffensive):
	def __str__(self):
		return "soul strike"


class DoubleBounty(BaseOffensive):
	def __str__(self):
		return "double bounty"


class BaseDestroyer(BaseOffensive):
	def __str__(self):
		return "base destroyer"


class BarrierBreak(BaseOffensive):
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to break enemy barrier"


class ShieldBreak(BaseOffensive):
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to break Aku shield"


class Critical(BaseOffensive):
	chance: int

	def __str__(self):
		return f"{self.chance}% chance to deal a critical hit"


class SavageBlow(BaseOffensive):
	chance: int
	amount: float

	def __str__(self):
		return f"{self.chance}% chance to deal a savage blow which does +{self.amount}% damage"


class Burrow(BaseOffensive):
	count: int
	distance: int

	def __str__(self):
		return f"burrows by {self.distance} up to {self.count} time/s"


class Conjure(BaseOffensive):
	spirit_id: int

	def __str__(self):
		return f"conjures spirit ID {self.spirit_id}"


class MetalKiller(BaseOffensive):
	percent: int

	def __str__(self):
		return f"deals metal killer damage equal to {self.percent}% of enemy's current HP"


class Passives(Model):
	immunities: list[Immunity] = field(default_factory=list)
	resists: list[Resist] = field(default_factory=list)
	defensives: list[Defensive] = field(default_factory=list)
	offensives: list[Offensive] = field(default_factory=list)
