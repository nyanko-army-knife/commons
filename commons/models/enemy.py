import serde
from copy import deepcopy
from typing import Self

from .entity import Entity

@serde.serde
class Enemy(Entity):
	id_: int = 0
	drop: int = 0

	def to_mag(self, hp: int, atk: int = 0) -> Self:
		atk = hp if atk == 0 else atk
		toret = deepcopy(self)
		toret.health = int(self.health * (hp / 100))
		toret.breakup = toret.breakup.scale(atk / 100)
		toret.damage = int(sum(hit.damage for hit in toret.breakup.hits()))
		return toret
