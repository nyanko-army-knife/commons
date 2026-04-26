import dataclasses
import itertools
from functools import reduce
from operator import attrgetter, add

from commons.models import Model


class StampItem(Model):
	category: int
	item: str
	item_qty: int


denylist = ('Cat CPU', 'Cat Jobs', 'Rich Cat', 'Sniper the Cat', 'Speed Up', 'Treasure Radar')


class Stamp(Model):
	id_: int
	unknown0: int
	unknown1: int
	unknown2: int
	unknown3: int
	unknown4: int
	items: list[list[StampItem]] = dataclasses.field(default_factory=list)

	def text(self):
		all_items = [item for set_ in self.items for item in set_]
		item_groups = itertools.groupby(sorted(all_items, key=attrgetter('item')), attrgetter('item'))
		counts = {}
		for item, instances in item_groups:
			counts[item] = sum(map(attrgetter('item_qty'), instances))
		return reduce(add, (t"{K}x{V}, " for K, V in counts.items() if K not in denylist))
