# only used for talents
from dataclasses import dataclass
from typing import TYPE_CHECKING

from commons.models.trait import Trait, PseudoTrait
from .base import Ability

if TYPE_CHECKING:
	from commons.models.unit import Form


@dataclass
class StatMod(Ability):
	def apply(self, cat: 'Form'):
		pass


@dataclass
class StatModAbs(StatMod):
	_klass = "stat_mod_abs"

	stat_name: str
	val: int

	def apply(self, cat: 'Form'):
		base_val = cat.__getattribute__(self.stat_name)
		new_val = base_val + self.val
		cat.__setattr__(self.stat_name, new_val)

	def __str__(self):
		return f"{self.val:+} {self.stat_name}"


@dataclass
class StatModRel(StatMod):
	_klass = "stat_mod_rel"

	stat_name: str
	val: int

	def apply(self, cat: 'Form'):
		base_val = cat.__getattribute__(self.stat_name)
		new_val = int(base_val * (1 + self.val / 100))
		cat.__setattr__(self.stat_name, new_val)

	def __str__(self):
		return f"{self.val:+}% {self.stat_name}"


@dataclass
class AddTargets(StatMod):
	_klass = "add_targets"

	traits: list[Trait]

	def apply(self, cat: 'Form'):
		cat.traits.extend(self.traits)

	def __str__(self):
		return f"adds target traits: {', '.join(self.traits)}"


@dataclass
class AddPTargets(StatMod):
	_klass = "add_ptargets"

	traits: list[PseudoTrait]

	def apply(self, cat: 'Form'):
		cat.ptraits.extend(self.traits)

	def __str__(self):
		return f"adds target pseudotraits: {', '.join(self.traits)}"
