from dataclasses import dataclass, field
from enum import Enum

from commons.models.abilities.base import Ability
from commons.models.base import Model


class Immunity(str, Enum):
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


class Resist(Ability):
  Wave: int = 0
  Knockback: int = 0
  Freeze: int = 0
  Slow: int = 0
  Weaken: int = 0
  Surge: int = 0
  Blast: int = 0
  Curse: int = 0


class Defensive(Ability):
  pass


@dataclass
class CounterSurge(Defensive):
  _klass = "counter_surge"

  def __str__(self):
    return f"has counter surge"


@dataclass
class WaveBlock(Defensive):
  _klass = "wave_block"

  def __str__(self):
    return f"has wave block"


@dataclass
class Barrier(Defensive):
  _klass = "barrier"
  health: int = 0

  def __str__(self):
    return f"barrier with {self.health} HP"


@dataclass
class Survive(Defensive):
  _klass = "survive"
  chance: int = 0

  def __str__(self):
    return f"{self.chance}% chance to survive a lethal attack"


@dataclass
class Shield(Defensive):
  _klass = "shield"
  health: int = 0
  regen: int = 0

  def __str__(self):
    return f"has an aku shield with {self.health} HP that regenerates by {self.regen}%"


@dataclass
class Revive(Defensive):
  _klass = "revive"
  count: int = 0
  delay: int = 0
  health: int = 0

  def __str__(self):
    return f"revives to {self.health}% after {self.delay}f up to {self.count} times"


@dataclass
class Strengthen(Defensive):
  _klass = "strengthen"
  health: int = 0
  mult: int = 0

  def __str__(self):
    return f"strengthens by +{self.mult}% at {self.health}% HP"


@dataclass
class BehemothDodge(Defensive):
  _klass = "behemoth_dodge"
  chance: int = 0
  duration: int = 0

  def __str__(self):
    return f"{self.chance}% chance to dodge behemoth attacks for {self.duration}f"


# --- #
@dataclass
class Offensive(Ability):
  pass


@dataclass
class Suicide(Offensive):
  _klass = "suicide"

  def __str__(self):
    return f"suicides on hit"


@dataclass
class Critical(Offensive):
  _klass = "critical"
  chance: int = 0

  def __str__(self):
    return f"{self.chance}% chance to deal a critical hit"


@dataclass
class SavageBlow(Offensive):
  _klass = "savage_blow"
  chance: int = 0
  amount: int = 0

  def __str__(self):
    return f"{self.chance}% chance to deal a savage blow which does +{self.amount}% damage"


@dataclass
class Burrow(Offensive):
  _klass = "burrow"
  count: int = 0
  distance: int = 0

  def __str__(self):
    return f"burrows by {self.distance} up to {self.count} time/s"


@dataclass
class Passives(Model):
  _klass = "passives"
  immunities: list[Immunity] = field(default_factory=list)
  resists: list[Resist] = field(default_factory=list)
  defensives: list[Defensive] = field(default_factory=list)
  offensives: list[Offensive] = field(default_factory=list)
