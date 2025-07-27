import itertools
from operator import attrgetter
from typing import Optional

import msgspec.json

from commons.models import Cat, Form, Gacha
from commons.models.combo import Combo, ComboCondition
from commons.models.enemy import Enemy
from commons.models.item import Item
from commons.models.stage import Category, Map, Stage
from commons.models.talents import Talent
from commons.utils.index import Index

enemies: Index[Enemy]
units: Index[Cat]
forms: Index[Form]
stages: Index[Stage]
maps: Index[Map]
categories: dict[str, Category]
combos: Index[Combo]
talents: dict[int, list[Talent]]
items: dict[int, Item]
gacha: dict[str, Gacha]


def load_cats():
	global units, forms

	with open('data/db/cats.json', mode='rb') as fl:
		c: list[Optional[Cat]] = msgspec.json.decode(fl.read(), type=list[Optional[Cat]])
	units = Index[Cat](c, lambda x: str(x.id_), {})
	forms = Index[Form](list(itertools.chain(*(cat.forms() for cat in c if cat is not None))), attrgetter("name"), {})


def load_enemies():
	global enemies

	with open('data/db/enemies.json') as fl:
		e = msgspec.json.decode(fl.read(), type=list[Enemy])
	enemies = Index[Enemy](e, attrgetter("name"), {})


def load_stages():
	global stages, maps, categories

	with open('data/db/stages.json') as fl:
		s = msgspec.json.decode(fl.read(), type=list[Category])
	stages = Index[Stage](list(itertools.chain(*(map_.stages for cat in s for map_ in cat.maps))), attrgetter("name"), {})
	maps = Index[Map](list(itertools.chain(*(cat.maps for cat in s))), attrgetter("name"), {})
	categories = {cat.id_: cat for cat in s}


def load_combos():
	global combos

	with open('data/db/combos.json') as fl:
		c = msgspec.json.decode(fl.read(), type=list[Combo])
	combos = Index[Combo]([combo for combo in c if combo.condition != ComboCondition.UNUSED], attrgetter("name"), {})


def load_talents():
	global talents

	with open('data/db/talents.json') as fl:
		talents = msgspec.json.decode(fl.read(), type=dict[int, list[Talent]])


def load_items():
	global items

	with open('data/db/items.json') as fl:
		items = {i.id_: i for i in msgspec.json.decode(fl.read(), type=list[Item])}


def load_gacha():
	global gacha

	with open('data/db/gachas.json') as fl:
		gacha = {f"{item.category}{item.id_:03}": item for item in
						 msgspec.json.decode(fl.read(), type=list[Gacha])}


def setup():
	load_cats()
	load_stages()
	load_enemies()
	load_combos()
	load_talents()
	load_items()
	load_gacha()
