import functools
from copy import deepcopy
from dataclasses import dataclass, field

from commons.models.abilities.active import ActiveAbility
from commons.models.abilities.extensions import Extension
from commons.models.abilities.mult import Mult
from commons.models.abilities.passive import Passives
from commons.models.attack_timing import AttackBreakup
from commons.models.base import Model
from commons.models.trait import PseudoTrait, Trait
from commons.utils.lazy import Lazy


@dataclass
class Form(Model):
  _klass = "form"
  id_: tuple[int, int] = None

  name: str = ""
  description: str = ""

  hp: int = 0
  kb: int = 0
  speed: int = 0
  atk: int = 0
  range_: int = 0
  cooldown: int = 0
  cost: int = 0
  hbox_offset: int = 0
  hbox_width: int = 0
  area_attack: bool = False

  traits: list[Trait] = None
  ptraits: list[PseudoTrait] = None
  extensions: list[Extension] = None
  abilities: list[ActiveAbility] = None
  passives: Passives = field(default_factory=Passives)
  breakup: AttackBreakup = field(default_factory=AttackBreakup)
  mults: list[Mult] = None

  def to_level(self, level: int, curve: list[int]) -> 'Form':
    toret = deepcopy(self)
    mult = 1 + sum(curve[i // 10] for i in range(1, level)) / 100
    toret.breakup = toret.breakup.scale(mult, 1.5)
    toret.atk = sum(hit.damage for hit in toret.breakup.hits())
    toret.hp = int(round(toret.hp * mult) * 2.5)
    toret.cost = int(toret.cost * 1.5)
    toret.cooldown = max(toret.cooldown * 2 - 264, 48)  # (research_level - 1) * 6 + treasures * 30
    return toret


@dataclass
class Cat(Model):
  _klass = "cat"
  id_: int = 0
  level_curve: list[int] = None

  form_base: Form = None
  form_evolved: Form = None
  form_true: Form = None
  form_ultra: Form = None

  def forms(self) -> list[Form]:
    return [form for form in (self.form_base, self.form_evolved, self.form_true, self.form_ultra) if form is not None]

  def to_level(self, level: int) -> 'Cat':
    toret = deepcopy(self)

    def apply_level_curve(level, curve):
      return lambda f: functools.partial(f, level, curve)
    fill_cat_curve = apply_level_curve(level, self.level_curve)

    # ill remove the lazy stuff if it's ever unstable
    if toret.form_base:
      toret.form_base = Lazy(fill_cat_curve(toret.form_base.to_level))
    if toret.form_evolved:
      toret.form_evolved = Lazy(fill_cat_curve(toret.form_evolved.to_level))
    if toret.form_true:
      toret.form_true = Lazy(fill_cat_curve(toret.form_true.to_level))
    if toret.form_ultra:
      toret.form_ultra = Lazy(fill_cat_curve(toret.form_ultra.to_level))
    return toret
