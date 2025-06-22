import functools
from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum

from commons.models.abilities.mult import Mult
from commons.models.base import Model
from commons.models.entity import Entity


class Rarity(IntEnum):
	NORMAL = 0
	SPECIAL = 1
	RARE = 2
	SUPER_RARE = 3
	UBER_RARE = 4
	LEGEND_RARE = 5

	@property
	def label(self):
		return self.name.title().replace("_", " ")


class UnlockMethod(IntEnum):
	STAGE = 0
	BUY = 1
	GACHA = 2

	@property
	def label(self):
		return self.name.title().replace("_", " ")


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
	xp_curve: list[int] = None
	rarity: Rarity = None
	tf_reqs: list[tuple[int, int]] = None
	tf_level: int = 0
	tf_xp: int = 0
	uf_reqs: list[tuple[int, int]] = None
	uf_level: int = 0
	uf_xp: int = 0
	max_level: tuple[int, int, int] = None  # max level, max level with catseyes, max plus level
	unlock_method: UnlockMethod = None

	form_base: Form = None
	form_evolved: Form = None
	form_true: Form = None
	form_ultra: Form = None

	@property
	def levelcap(self):
		return self.max_level[1] + self.max_level[2]

	def forms(self) -> list[Form]:
		return [form for form in (self.form_base, self.form_evolved, self.form_true, self.form_ultra) if form is not None]

	def form_to_level(self, try_form_id: int, try_level: int, upcast: bool = False) -> (Form, int):
		"""
		will downcast level to max level and return said level.
		will downcast forms if level is insufficient.
		if told to upcast, will upcast level instead of downcasting form.
		"""
		try_level = min(try_level, self.levelcap)
		try_form_id %= len(self.forms())
		level, form_id = try_level, try_form_id

		if not upcast:  # we are sure about level
			if level < 10:
				form_id = 0
			elif level < max(20, self.tf_level):
				form_id = min(1, try_form_id)
			elif level < self.uf_level:
				form_id = min(2, try_form_id)
		else:  # we are sure about form_id
			if form_id == 1 and try_level < 10:
				level = 10
			if try_form_id == 2 and try_level < max(20, self.tf_level):
				level = max(20, self.tf_level)
			elif try_form_id == 3 and try_level < self.uf_level:
				level = self.uf_level
		return self[form_id].to_level(level, self.level_curve), level

	def to_level(self, level: int) -> 'Cat':
		toret = deepcopy(self)

		def apply_level_curve(to_level: int, curve):
			return lambda f: functools.partial(f, to_level, curve)

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
