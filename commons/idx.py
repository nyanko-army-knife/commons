import itertools
import json
from operator import attrgetter
from typing import Optional

import msgspec.json
import serde.json
from typing import Any

from commons.models import Cat, Form, Gacha, FormID
from commons.models.combo import Combo, ComboCondition
from commons.models.enemy import Enemy
from commons.models.item import Item
from commons.models.stage import Category, Map, Stage
from commons.models.stamp import Stamp
from commons.models.talents import Talent, UnitTalents
from commons.utils import msg
from commons.utils.index import Index

enemies: Index[Enemy]
units: Index[Cat]
forms: Index[Form]
stages: Index[Stage]
maps: Index[Map]
categories: dict[str, Category]
combos: Index[Combo]
talents: dict[int, UnitTalents]
items: dict[int, Item]
items_by_server_id: dict[int, Item]
sales: dict[int, str]
stamps: dict[int, Stamp]
gacha: dict[str, Gacha]


def load_cats():
	global units, forms
	pass

	with open('data/db/cats.json', 'rb') as fl:
		c: list[Optional[Cat]] = serde.json.from_json(list[Optional[Cat]], fl.read())

	for i, cat in enumerate(c):
		if cat is None: continue
		cat.id_ = i
		for j, form in enumerate(cat.forms()):
			form.id_ = (i, FormID(j))

	units = Index[Cat](c, lambda x: str(x.id_), None)
	forms = Index[Form](list(itertools.chain(*(cat.forms() for cat in c if cat is not None))), attrgetter("name"),
											lambda x: x.aliases)


def load_enemies():
	global enemies

	with open('data/db/enemies.json') as fl:
		ex: list[Optional[Enemy]] = serde.json.from_json(list[Optional[Enemy]], fl.read())
	for i, e in enumerate(ex):
		if e is not None:
			e.id_ = i
	enemies = Index[Enemy](ex, attrgetter("name"), attrgetter("aliases"))


def load_stages():
	global stages, maps, categories

	with open('data/db/stages.json') as fl:
		s = msgspec.json.decode(fl.read(), type=list[Category])
	stages = Index[Stage](list(itertools.chain(*(map_.stages for cat in s for map_ in cat.maps))), attrgetter("name"), None)
	maps = Index[Map](list(itertools.chain(*(cat.maps for cat in s))), attrgetter("name"), None)
	categories = {cat.id_: cat for cat in s}


def load_combos():
	global combos

	with open('data/db/combos.json') as fl:
		c = msgspec.json.decode(fl.read(), type=list[Combo])
	combos = Index[Combo]([combo for combo in c if combo.condition != ComboCondition.UNUSED], attrgetter("name"), None)


def load_talents():
	global talents

	with open('data/db/talents.json') as fl:
		talents = serde.json.from_json(dict[int, UnitTalents], fl.read())


def load_items():
	global items
	global items_by_server_id

	with open('data/db/items.json') as fl:
		items = {i.id_: i for i in msgspec.json.decode(fl.read(), type=list[Item])}

	with open('data/db/items.json') as fl:
		items_by_server_id = {i.server_id: i for i in msgspec.json.decode(fl.read(), type=list[Item])}


def load_gacha():
	global gacha

	with open('data/db/gachas.json') as fl:
		gacha = {f"{item.category}{item.id_:04}": item for item in
						 msgspec.json.decode(fl.read(), type=list[Gacha])}


def load_sales():
	global sales

	with open('data/db/sales.json') as fl:
		sales = {int(k): v for k, v in json.loads(fl.read()).items()}


def load_stamps():
	global stamps

	with open('data/db/stamps.json') as fl:
		s = msg.dec(list[Stamp]).decode(fl.read())
	stamps = {stamp.id_: stamp for stamp in s}


def setup():
	load_cats()
	load_stages()
	load_enemies()
	load_combos()
	load_talents()
	load_items()
	load_gacha()
	load_sales()
	load_stamps()
