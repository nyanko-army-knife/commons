from copy import deepcopy
from typing import Self

from .entity import Entity


class Enemy(Entity):
	id_: int = 0
	drop: int = 0

	def to_mag(self, hp: int, atk: int = 0) -> Self:
		atk = hp if atk == 0 else atk
		toret = deepcopy(self)
		toret.hp = int(self.hp * (hp / 100))
		toret.breakup = toret.breakup.scale(atk / 100)
		toret.atk = int(sum(hit.damage for hit in toret.breakup.hits()))
		return toret
