import difflib
from typing import Callable


class Index[T]:
	items: list[T]
	lookup_dict: dict[str, T]

	def __getitem__(self, item) -> T:
		return self.items[item]

	def __init__(self, items: list[T], namegetter: Callable[[T], str], aliases: dict[str, int]):
		self.items = items
		self.lookup_dict = {namegetter(x).lower(): x for x in items if x is not None} | {K.lower(): items[V] for K, V in aliases.items()}
		self.namegetter = namegetter

	def lookup(self, target: str) -> T:
		name = difflib.get_close_matches(target.lower(), self.lookup_dict.keys(), cutoff=0)[0]
		return self.lookup_dict[name]

	def get(self, id_: int) -> T:
		return self.items[id_]
