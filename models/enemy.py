from dataclasses import dataclass, field

from commons.models.abilities.active import ActiveAbility
from commons.models.abilities.extensions import Extension
from commons.models.abilities.passive import Passives
from commons.models.attack_timing import AttackBreakup
from commons.models.base import Model
from commons.models.trait import PseudoTrait, Trait
from commons.utils.index import Index


@dataclass
class Enemy(Model):
  _klass = "enemy"

  id_: int = 0
  name: str = ""
  description: str = ""

  hp: int = 0
  kb: int = 0
  speed: int = 0
  atk: int = 0
  range_: int = 0
  drop: int = 0
  hbox_offset: int = 0
  hbox_width: int = 0
  area_attack: bool = False

  traits: list[Trait] = field(default_factory=list)
  ptraits: list[PseudoTrait] = field(default_factory=list)
  extensions: list[Extension] = field(default_factory=list)
  abilities: list[ActiveAbility] = field(default_factory=list)
  passives: Passives = field(default_factory=Passives)
  breakup: AttackBreakup = field(default_factory=AttackBreakup)


enemies: Index[Enemy] = None
