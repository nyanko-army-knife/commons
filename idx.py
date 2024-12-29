import itertools
import json
from operator import attrgetter

from commons.models.combo import Combo, ComboSize, ComboEffect
from commons.models.enemy import Enemy
from commons.models.lookup import object_hook_ability
import commons.models.lookup as lookup
from commons.models.stage import Category, Map, Stage
from commons.models.unit import Form, Cat
from commons.utils.index import Index

enemies: Index[Enemy]
units: list[Cat]
forms: Index[Form]
stages: Index[Stage]
maps: Index[Map]
categories: dict[str, Category]

emojis: dict[str, int]

def setup():
  lookup.setup()
  global enemies, units, forms, stages, maps, categories, emojis

  with open('data/db/enemies.json') as fl:
    e: list[Enemy] = json.load(fl, object_hook=object_hook_ability)
  enemies = Index[Enemy](e, attrgetter("name"), {})

  with open('data/db/cats.json') as fl:
    c: list[Cat] = json.load(fl, object_hook=object_hook_ability)
  units = c
  forms = Index[Form](list(itertools.chain(*(cat.forms() for cat in c if cat is not None))), attrgetter("name"), {})

  with open('data/db/stages.json') as fl:
    s: list[Category] = json.load(fl, object_hook=object_hook_ability)
  stages = Index[Stage](
    list(itertools.chain(*(map_.stages for cat in s for map_ in cat.maps))),
    attrgetter("name"),
    {}
  )
  maps = Index[Map](list(itertools.chain(*(cat.maps for cat in s))), attrgetter("name"), {})
  categories = {cat.id_: cat for cat in s}

  combos: Index[Combo] = None  # TODO
  combos_with: dict[int, list[tuple[int, Combo]]] = None
  combo_sizes: list[ComboSize] = []
  combo_effects: list[ComboEffect] = []

  with open('catbot/assets_cache/emojis.json') as fl:
    emojis = json.load(fl)
