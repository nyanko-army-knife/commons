from unittest import skip
from commons.models.base import intenum_field, strenum_list_field
import serde
import functools
from copy import deepcopy
from enum import IntEnum
from typing import Optional, Self

from msgspec import field

from commons.models import Model, Duration
from commons.models.abilities.mult import Mult
from commons.models.entity import Entity


class Rarity(IntEnum):
	Normal = 0
	Special = 1
	Rare = 2
	SuperRare = 3
	UberRare = 4
	LegendRare = 5

	@property
	def label(self):
		return self.name


class UnlockMethod(IntEnum):
	Stage = 0
	Buy = 1
	Gacha = 2

	@property
	def label(self):
		return self.name


class FormID(IntEnum):
	BASE = 0
	EVOLVED = 1
	TRUE = 2
	ULTRA = 3

	@property
	def label(self):
		return self.name.title()


@serde.serde(skip_if_default=True)
class Form(Entity):
	id_: tuple[int, FormID] = (-1, FormID.BASE)

	mults: list[Mult] = strenum_list_field(cls=Mult)
	cooldown: Duration = Duration(0)
	alternate_cooldown: int = 0  # could also be Optional[int], but int works directly into statmod
	cost: int = 0

	def to_level(self, level: int, curve: list[int]) -> Self:
		toret = deepcopy(self)
		mult = 1 + sum(curve[i // 10] for i in range(1, level)) / 100
		toret.breakup = toret.breakup.scale(mult, 1.5)
		toret.damage = int(sum(hit.damage for hit in toret.breakup.hits()))
		toret.health = int(round(toret.health * mult) * 2.5)
		toret.cooldown = Duration(max(toret.cooldown * 2 - 264, 48))  # (research_level - 1) * 6 + treasures * 30
		return toret

	@property
	def id_char(self):
		return 'fcsu'[self.id_[-1]]

@serde.serde(skip_if_default=True)
class Cat:
	id_: int = 0
	level_curve: list[int] = serde.field(default_factory=list)
	xp_curve: list[int] = serde.field(default_factory=list)
	rarity: Rarity = intenum_field(Rarity)
	tf_reqs: list[tuple[int, int]] = serde.field(default_factory=list)
	tf_level: int = 0
	tf_xp: int = 0
	uf_reqs: list[tuple[int, int]] = serde.field(default_factory=list)
	uf_level: int = 0
	uf_xp: int = 0
	guide_order: int = 0
	max_levels: tuple[int, int, int] = (-1, -1, -1)  # max level, max level with catseyes, max plus level
	unlock_method: UnlockMethod = intenum_field(UnlockMethod)

	base_form: Optional[Form] = None
	evolved_form: Optional[Form] = None
	true_form: Optional[Form] = None
	ultra_form: Optional[Form] = None

	@property
	def levelcap(self):
		return self.max_levels[1] + self.max_levels[2]

	def forms(self) -> list[Form]:
		return [form for form in (self.base_form, self.evolved_form, self.true_form, self.ultra_form) if form is not None]

	def form_to_level(self, try_form_id: int, try_level: int, upcast: bool = False) -> tuple[Form, int]:
		"""
		will downcast level to max level and return said level.
		will downcast forms if level is insufficient.
		if told to upcast, will upcast level instead of downcasting form.
		"""
		try_level = min(try_level, self.levelcap)
		try_form_id = try_form_id % len(self.forms())
		level, form_id = try_level, try_form_id

		if not upcast:  # we are sure about level
			if level < 10:
				form_id = FormID.BASE.value
			elif level < max(20, self.tf_level):
				form_id = FormID.EVOLVED.value
			elif self.uf_level < 0 or level < self.uf_level:
				form_id = FormID.TRUE.value
			else:
				form_id = FormID.ULTRA.value
		else:  # we are sure about form_id
			if form_id == FormID.EVOLVED and try_level < 10:
				level = 10
			if try_form_id == FormID.TRUE and try_level < max(20, self.tf_level):
				level = max(20, self.tf_level)
			elif try_form_id == FormID.ULTRA and try_level < self.uf_level:
				level = self.uf_level
		form_id = min(form_id, len(self.forms()) - 1)
		return self[form_id].to_level(level, self.level_curve), level

	def to_level(self, level: int) -> Self:
		toret = deepcopy(self)

		def apply_level_curve(to_level: int, curve):
			return lambda f: functools.partial(f, to_level, curve)

		fill_cat_curve = apply_level_curve(level, self.level_curve)

		if toret.base_form:
			toret.base_form = fill_cat_curve(toret.base_form.to_level)()
		if toret.evolved_form:
			toret.evolved_form = fill_cat_curve(toret.evolved_form.to_level)()
		if toret.true_form:
			toret.true_form = fill_cat_curve(toret.true_form.to_level)()
		if toret.ultra_form:
			toret.ultra_form = fill_cat_curve(toret.ultra_form.to_level)()
		return toret

	def __getitem__(self, item):
		return self.forms()[item]
