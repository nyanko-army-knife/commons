from commons.utils.index import ALGO_SLOW
from rapidfuzz import process
from rapidfuzz.fuzz import QRatio, WRatio, token_set_ratio, partial_ratio, partial_token_set_ratio, partial_token_sort_ratio, token_sort_ratio
import os
import unittest

from commons import idx

corpus: list[str] = [""]

def test_lookup(subtests):
	PAIRS = [
		("dark lazer", "Dark Lazer"),
		("mohawk", "Mohawk Cat"),
		("manic island", "Manic Island Cat"),
		("meraser", "Manic Eraser Cat"),
		("lil eraser", "Li'l Eraser Cat"),
		("uril", "Master Uril"),
		("red Ranger", "Red Nyanko Ranger"),
		("green ranger", "Green Nyanko Ranger"),
		("pink ranger", "Pink Nyanko Ranger"),
		("blue ranger", "Blue Nyanko Ranger"),
		("yelo ragte", "Yellow Nyanko Ranger"),
		("balrog", "Greater Balrog Cat")
	]
	idx.load_cats()

	for (inp, out) in PAIRS:
		with subtests.test(msg=f"{inp} -> {out}"):
			u = idx.forms.lookup(inp)
			assert u is not None
			try:
				assert u.name == out
			except AssertionError as e:
				print(idx.forms.lookup_debug(inp))
				raise e
