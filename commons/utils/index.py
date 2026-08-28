import typing
from functools import lru_cache
from typing import Callable

import rapidfuzz


class Lookup(typing.NamedTuple):
	name: str
	score: float
	key: int

def algo_slow(a, b, *, processor=None, score_cutoff=None):
	# we don't pass score_cutoff into individual algorithms because that would cause premature termination.
	x = rapidfuzz.fuzz.WRatio(a, b, processor=processor)
	y = rapidfuzz.fuzz.partial_token_sort_ratio(a, b, processor=processor)
	z = rapidfuzz.fuzz.token_set_ratio(a, b, processor=processor)
	return (x*2 + y*4 + z*4)/10

QUICK_THRESHOLD = 80
ALGO_QUICK = rapidfuzz.fuzz.ratio
SLOW_THRESHOLD = 50
ALGO_SLOW = algo_slow

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
			self.lookup_dict |= {alias.lower(): x for x in items if x is not None for alias in aliasgetter(x)}
		self.namegetter = namegetter

	@lru_cache(maxsize=1 << 10)
	def lookup(self, target: str) -> T:
		"""loads closest item in index to target string"""

		target = target.lower()
		(name, score, _key) = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=ALGO_QUICK)
		if score < QUICK_THRESHOLD:
			name, _score, _key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=ALGO_SLOW)
		return self.lookup_dict[name]

	@lru_cache(maxsize=1 << 10)
	def lookup_with_score(self, target: str) -> tuple[T, float]:
		target = target.lower()
		(name, score, _key) = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=ALGO_QUICK)
		if score < QUICK_THRESHOLD:
			name, score, _key = rapidfuzz.process.extractOne(target, self.lookup_dict.keys(), scorer=ALGO_SLOW)
		return (self.lookup_dict[name], score)

	@lru_cache(maxsize=1 << 10)
	def lookup_debug(self, target: str, force_quick: bool = False) -> tuple[bool, list[Lookup]]:
		target = target.lower()
		lookups: list[Lookup] = [Lookup(*x) for x in
														 rapidfuzz.process.extract(target, self.lookup_dict.keys(), scorer=ALGO_QUICK)]
		if lookups[0].score > QUICK_THRESHOLD or force_quick:
			return True, lookups
		lookups = [Lookup(*x) for x in rapidfuzz.process.extract(target, self.lookup_dict.keys(), scorer=ALGO_SLOW)]
		return False, lookups

	def get(self, id_: int) -> T:
		return self.items[id_]
