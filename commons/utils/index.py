import typing
from functools import lru_cache
from typing import Callable

import rapidfuzz


class Lookup(typing.NamedTuple):
	name: str
	score: float
	key: str


QUICK_THRESHOLD = 80
SLOW_THRESHOLD = 70


class Index[T]:
	items: list[T]
	lookup_dict: dict[str, T]

	def __getitem__(self, item) -> T:
		return self.items[item]

	def __init__(self, items: list[T], namegetter: Callable[[T], str],
							 aliasgetter: typing.Optional[Callable[[T], list[str]]]):
		self.items = items
		self.lookup_dict = {namegetter(x).lower(): x for x in items if x is not None}
		if aliasgetter:
			self.lookup_dict |= {alias: x for x in items if x is not None for alias in aliasgetter(x)}
		self.namegetter = namegetter

	@lru_cache(maxsize=1 << 10)
	def lookup(self, target: str) -> T:
		target = target.lower()
		# noinspection PyTypeChecker
		name, score, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=rapidfuzz.fuzz.QRatio)
		if score >= QUICK_THRESHOLD:
			return self.lookup_dict[name]
		else:
			name, score, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys())
			return self.lookup_dict[name]

	@lru_cache(maxsize=1 << 10)
	def lookup_with_score(self, target: str) -> tuple[T, float]:
		target = target.lower()
		# noinspection PyTypeChecker
		name, score, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=rapidfuzz.fuzz.QRatio)
		if score >= QUICK_THRESHOLD:
			return self.lookup_dict[name], score
		else:
			name, _, key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys())
			return self.lookup_dict[name], rapidfuzz.fuzz.QRatio(target, name)

	@lru_cache(maxsize=1 << 10)
	def lookup_debug(self, target: str, force_quick: bool = False) -> tuple[bool, list[Lookup]]:
		target = target.lower()
		# noinspection PyTypeChecker
		lookups: list[Lookup] = [Lookup(*x) for x in
														 rapidfuzz.process.extract(target, self.lookup_dict.keys(), scorer=rapidfuzz.fuzz.QRatio)]
		if lookups[0].score >= QUICK_THRESHOLD or force_quick:
			return True, lookups

		lookups = [Lookup(*x) for x in rapidfuzz.process.extract(target, self.lookup_dict.keys())]
		return False, lookups

	def get(self, id_: int) -> T:
		return self.items[id_]
