from commons.models.abilities import Passives
from commons.models.abilities import Extension, ActiveAbility
import serde

from commons.models import AttackBreakup
from commons.models.base import bitflag_field
from commons.models.trait import PseudoTraits, Traits


@serde.serde(skip_if_default=True, skip_if_none=True)
class Entity:
	name: str
	description: list[str]

	health: int
	knockbacks: int
	speed: int # TODO: make custom speed unit
	damage: int
	standing_range: int
	# hbox_offset: int
	# hbox_width: int
	area_targeting: bool

	extensions: Extension = serde.field(flatten=True, skip_if_default=True)
	actives: ActiveAbility = serde.field(flatten=True, skip_if_default=True)
	passives: Passives = serde.field(flatten=True, skip_if_default=True)
	traits: Traits = bitflag_field(Traits)
	pseudotraits: PseudoTraits = bitflag_field(PseudoTraits)
	aliases: list[str] = serde.field(default_factory=list)

	breakup: AttackBreakup = serde.field(default_factory=AttackBreakup)

	@property
	def dps(self) -> float:
		return 30 * self.damage / self.breakup.cd_effective
