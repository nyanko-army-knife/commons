from enum import Flag
import dataclasses
from dataclasses import dataclass
from commons.models.trait import Traits, PseudoTraits
import serde
from functools import reduce
from operator import add
from typing import TYPE_CHECKING, Optional, Any

from commons import c
from commons.models.base import Model, bitflag_field
from ..abilities import ActiveAbility, Extension, Slow, Freeze, Weaken, Wave, Proc, Immunity, Strengthen, Survive, Surge, TargetOnly, Knockback, BaseDestroyer, Critical, ZombieKiller, BarrierBreak, DoubleBounty, WaveBlock, Dodge, SavageBlow, ShieldBreak, Curse, Blast, CounterSurge, AddMult, Targets, PseudoTargets, SoulStrike, BehemothDodge
from ..abilities import (
	BaseDefensives,
	BaseOffensives,
	BaseStatMod,
	Resist,
	StatMod,
)
from ..unit import Form


type Effect = Weaken | Freeze | Slow | Wave | StatMod | Immunity | Strengthen | Survive | Targets | Surge | TargetOnly | Knockback | Resist | PseudoTargets | BaseDestroyer | Critical | ZombieKiller | BarrierBreak | DoubleBounty | WaveBlock | Dodge | SavageBlow | Surge | ShieldBreak | Curse | Blast | CounterSurge | AddMult | SoulStrike | BehemothDodge

def lerp_level[E: Effect](start: E, end: E, amount: float) -> E:
	# if not (max_level >= level > 0): level = max_level
	if amount == 0: return start
	if amount == 1: return end

	out = start
	for field in dataclasses.fields(start):
		start_val, end_val = getattr(start, field.name), getattr(end, field.name)
		try:
			interp_val = start_val + int((end_val - start_val) * amount)
		except TypeError:
			interp_val = start_val
		setattr(out, field.name, interp_val)
	return out


@serde.serde
class Talent:
	target: str
	effect_min: Effect
	effect_max: Effect
	np_curve: list[int]
	name: str
	text: str
	max_level: int = 10
	is_ultra: bool = False
	applied_traits: Traits = bitflag_field(Traits)

	def apply_level_to(self, level: int, cat: 'Form') -> 'Form':
		def update_at(obj: Any, target: str, value: Any):
			steps = target.split(".")
			if steps[0] in ("immunities", "resistances", "defensives", "offensives"):
				steps.insert(0,"passives")

			target_node = obj
			for step in steps[:-1]:
				target_node = getattr(target_node, step)

			old_val = getattr(target_node, steps[-1])
			new_val = value
			if isinstance(old_val, list):
				new_val = old_val + [value]
			elif isinstance(old_val, Flag):
				new_val = old_val | value

			setattr(target_node, steps[-1], new_val)


		def get_at(obj: Any, target: str):
			target_node = obj
			for step in target.split("."):
				target_node = getattr(target_node, step, None)
			return target_node


		e = lerp_level(self.effect_min, self.effect_max, level/self.max_level)
		if isinstance(e, StatMod):
			curr = get_at(cat, self.target)
			final = int(curr * (1+e.amount/100)) if e.relative else curr + e.amount
			update_at(cat, self.target, final)
		elif isinstance(e, AddMult):
			update_at(cat, self.target, e.mult)
		elif dataclasses.is_dataclass(e):
			update_at(cat, self.target, e)

		if self.applied_traits:
			cat.traits |= self.applied_traits

		return cat


@serde.serde
class UnitTalents:
	talents: list[Talent]
