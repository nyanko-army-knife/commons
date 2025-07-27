from msgspec import field

from commons.models.abilities import ActiveAbility, Extension, Passives
from commons.models.attack_timing import AttackBreakup
from commons.models.base import Model
from commons.models.trait import PseudoTrait, Trait


class Entity(Model):
	name: str = ""
	description: str = ""

	hp: int = 0
	kb: int = 0
	speed: int = 0
	atk: int = 0
	range_: int = 0
	hbox_offset: int = 0
	hbox_width: int = 0
	area_attack: bool = False

	traits: list[Trait] = field(default_factory=list)
	ptraits: list[PseudoTrait] = field(default_factory=list)
	extensions: list[Extension] = field(default_factory=list)
	abilities: list[ActiveAbility] = field(default_factory=list)
	passives: Passives = field(default_factory=Passives)
	breakup: AttackBreakup = field(default_factory=AttackBreakup)
