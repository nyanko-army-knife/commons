from functools import lru_cache
from typing import Callable

import rapidfuzz


class Index[T]:
	items: list[T]
	lookup_dict: dict[str, T]

	def __getitem__(self, item) -> T:
		return self.items[item]

	def __init__(self, items: list[T], namegetter: Callable[[T], str], aliases: dict[str, int]):
		self.items = items
		self.lookup_dict = ({namegetter(x).lower(): x for x in items if x is not None}
												| {K.lower(): items[V] for K, V in aliases.items()})
		self.namegetter = namegetter

	@lru_cache(maxsize=1 << 10)
	def lookup(self, target: str) -> T:
		# noinspection PyTypeChecker
		name, score, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=rapidfuzz.fuzz.QRatio)
		if score > 85:
			return self.lookup_dict[name]
		else:
			name, score, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys())
			return self.lookup_dict[name]

	@lru_cache(maxsize=1 << 10)
	def lookup_with_score(self, target: str) -> tuple[T, float]:
		# noinspection PyTypeChecker
		name, score, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=rapidfuzz.fuzz.QRatio)
		if score > 85:
			return self.lookup_dict[name], score
		else:
			name, _, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys())
			return self.lookup_dict[name], rapidfuzz.fuzz.QRatio(target, name)

	def get(self, id_: int) -> T:
		return self.items[id_]
