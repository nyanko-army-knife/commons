# only used for talents
from dataclasses import dataclass

from commons.models.base import Model
from commons.models.trait import Trait, PseudoTrait


@dataclass
class StatModAbs(Model):
	_klass = "stat_mod_abs"

	stat_name: str
	val: int

	def apply(self, cat: 'Cat'):
		base_val = cat.__getattribute__(self.stat_name)
		new_val = base_val + self.val
		cat.__setattr__(self.stat_name, new_val)

	def __str__(self):
		return f"{self.val:+} {self.stat_name}"


@dataclass
class StatModRel(Model):
	_klass = "stat_mod_rel"

	stat_name: str
	val: int

	def apply(self, cat: 'Cat'):
		base_val = cat.__getattribute__(self.stat_name)
		new_val = base_val * (1 + self.val / 100)
		cat.__setattr__(self.stat_name, new_val)

	def __str__(self):
		return f"{self.val:+}% {self.stat_name}"


@dataclass
class AddTargets(Model):
	_klass = "add_targets"

	traits: list[Trait]

	def __str__(self):
		return f"adds target traits: {', '.join(self.traits)}"


@dataclass
class AddPTargets(Model):
	_klass = "add_ptargets"

	traits: list[PseudoTrait]

	def __str__(self):
		return f"adds target pseudotraits: {', '.join(self.traits)}"
