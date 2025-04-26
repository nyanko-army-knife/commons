import functools
from copy import deepcopy
from dataclasses import dataclass

from commons.models.abilities.mult import Mult
from commons.models.base import Model
from commons.models.entity import Entity


@dataclass(kw_only=True)
class Form(Entity):
	_klass = "form"
	id_: tuple[int, int] = None

	mults: list[Mult] = None
	cooldown: int = 0
	cost: int = 0

	def to_level(self, level: int, curve: list[int]) -> 'Form':
		toret = deepcopy(self)
		mult = 1 + sum(curve[i // 10] for i in range(1, level)) / 100
		toret.breakup = toret.breakup.scale(mult, 1.5)
		toret.atk = int(sum(hit.damage for hit in toret.breakup.hits()))
		toret.hp = int(round(toret.hp * mult) * 2.5)
		toret.cost = int(toret.cost * 1.5)
		toret.cooldown = max(toret.cooldown * 2 - 264, 48)  # (research_level - 1) * 6 + treasures * 30
		return toret

	@property
	def id_char(self):
		return 'fcsu'[self.id_[-1]]


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

		def apply_level_curve(l: int, curve):
			return lambda f: functools.partial(f, l, curve)

		fill_cat_curve = apply_level_curve(level, self.level_curve)

		if toret.form_base:
			toret.form_base = fill_cat_curve(toret.form_base.to_level)()
		if toret.form_evolved:
			toret.form_evolved = fill_cat_curve(toret.form_evolved.to_level)()
		if toret.form_true:
			toret.form_true = fill_cat_curve(toret.form_true.to_level)()
		if toret.form_ultra:
			toret.form_ultra = fill_cat_curve(toret.form_ultra.to_level)()
		return toret

	def __getitem__(self, item):
		return self.forms()[item]
