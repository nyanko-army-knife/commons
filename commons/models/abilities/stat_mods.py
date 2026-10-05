# only used for talents
import commons.models.abilities.mult as mult
from commons.models.base import bitflag_field, strenum_field
import serde
import functools
from typing import TYPE_CHECKING

from commons.models.trait import PseudoTraits, Traits
from .base import Ability
from .mult import Mult

if TYPE_CHECKING:
	from commons.models.unit import Form


class BaseStatMod(Ability):
	def apply(self, cat: 'Form'):
		pass


@serde.serde
class StatMod:
	amount: int
	relative: bool

	def __str__(self):
		return f"{self.amount:+}"


@serde.serde(transparent=True)
class Targets:
	traits: Traits = bitflag_field(Traits)

	def __ror__(self, t: Traits):
		return t | self.traits


@serde.serde(transparent=True)
class PseudoTargets:
	ptraits: PseudoTraits = bitflag_field(PseudoTraits)

	def __ror__(self, t: PseudoTraits):
		return t | self.ptraits

# wrapper that gives serde functionalities to mult talent
@serde.serde(transparent=True)
class AddMult:
	mult: Mult = strenum_field(Mult)
