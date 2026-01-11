from msgspec import field

from commons.models.abilities import ActiveAbility, Extension, Passives
from commons.models.attack_timing import AttackBreakup
from commons.models.base import Model
from commons.models.trait import PseudoTrait, Trait


class Entity(Model):
	name: str
	aliases: list[str]
	description: str

	hp: int
	kb: int
	speed: int
	atk: int
	range_: int
	hbox_offset: int
	hbox_width: int
	area_attack: bool

	traits: list[Trait] = field(default_factory=list)
	ptraits: list[PseudoTrait] = field(default_factory=list)
	extensions: list[Extension] = field(default_factory=list)
	abilities: list[ActiveAbility] = field(default_factory=list)
	passives: Passives = field(default_factory=Passives)
	breakup: AttackBreakup = field(default_factory=AttackBreakup)
