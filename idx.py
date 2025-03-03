import itertools
import json
from operator import attrgetter

import commons.models.lookup as lookup
from commons.models import Cat, Form
from commons.models.combo import Combo, ComboCondition
from commons.models.enemy import Enemy
from commons.models.lookup import object_hook_ability
from commons.models.stage import Category, Map, Stage
from commons.models.talents import Talent
from commons.utils.index import Index

lookup.setup()

enemies: Index[Enemy]
units: list[Cat]
forms: Index[Form]
stages: Index[Stage]
maps: Index[Map]
categories: dict[str, Category]
combos: Index[Combo]
talents: dict[int, list[Talent]]


def load_cats():
	global units, forms

	with open('data/db/cats.json') as fl:
		c: list[Cat] = json.load(fl, object_hook=object_hook_ability)
	units = c
	forms = Index[Form](list(itertools.chain(*(cat.forms() for cat in c if cat is not None))), attrgetter("name"), {})


def load_enemies():
	global enemies

	with open('data/db/enemies.json') as fl:
		e: list[Enemy] = json.load(fl, object_hook=object_hook_ability)
	enemies = Index[Enemy](e, attrgetter("name"), {})


def load_stages():
	global stages, maps, categories

	with open('data/db/stages.json') as fl:
		s: list[Category] = json.load(fl, object_hook=object_hook_ability)
	stages = Index[Stage](list(itertools.chain(*(map_.stages for cat in s for map_ in cat.maps))), attrgetter("name"), {})
	maps = Index[Map](list(itertools.chain(*(cat.maps for cat in s))), attrgetter("name"), {})
	categories = {cat.id_: cat for cat in s}


def load_combos():
	global combos

	with open('data/db/combos.json') as fl:
		c = json.load(fl, object_hook=object_hook_ability)
	print([x.name for x in c if type(x.name) == float])
	combos = Index[Combo]([combo for combo in c if combo.condition != ComboCondition.UNUSED], attrgetter("name"), {})


def load_talents():
	global talents

	with open('data/db/talents.json') as fl:
		talents = {int(k): v for k, v in json.load(fl, object_hook=object_hook_ability).items()}


def setup():
	global enemies, units, forms, stages, maps, categories

	load_cats()
	load_stages()
	load_enemies()
	load_combos()
	load_talents()
