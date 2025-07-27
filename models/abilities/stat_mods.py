# only used for talents
from typing import TYPE_CHECKING

from commons.models.trait import PseudoTrait, Trait

from .base import Ability
from .mult import Mult

if TYPE_CHECKING:
	from commons.models.unit import Form


class BaseStatMod(Ability):
	def apply(self, cat: 'Form'):
		pass


type StatMod = StatModAbs | StatModRel | AddTargets | AddPTargets | AddMults


class StatModAbs(BaseStatMod):
	stat_name: str
	val: int

	def apply(self, cat: 'Form'):
		base_val = cat.__getattribute__(self.stat_name)
		new_val = base_val + self.val
		cat.__setattr__(self.stat_name, new_val)

	def __str__(self):
		return f"{self.val:+} {self.stat_name}"


class StatModRel(BaseStatMod):
	stat_name: str
	val: int

	def apply(self, cat: 'Form'):
		base_val = cat.__getattribute__(self.stat_name)
		new_val = int(base_val * (1 + self.val / 100))
		cat.__setattr__(self.stat_name, new_val)

	def __str__(self):
		return f"{self.val:+}% {self.stat_name}"


class AddTargets(BaseStatMod):
	traits: list[Trait]

	def apply(self, cat: 'Form'):
		cat.traits.extend(self.traits)

	def __str__(self):
		return f"adds target traits: {', '.join(self.traits)}"


class AddPTargets(BaseStatMod):
	traits: list[PseudoTrait]

	def apply(self, cat: 'Form'):
		cat.ptraits.extend(self.traits)

	def __str__(self):
		return f"adds target pseudotraits: {', '.join(self.traits)}"


class AddMults(BaseStatMod):
	mults: list[Mult]

	def apply(self, cat: 'Form'):
		cat.mults.extend(self.mults)

	def __str__(self):
		return f"adds effectiveness: {', '.join(self.mults)}"
