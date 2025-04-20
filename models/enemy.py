from copy import deepcopy
from dataclasses import dataclass

from .entity import Entity


@dataclass(kw_only=True)
class Enemy(Entity):
	_klass: str = "enemy"

	id_: int = 0
	drop: int = 0

	def to_mag(self, hp: int, atk: int = 0) -> 'Enemy':
		atk = hp if atk == 0 else atk
		toret = deepcopy(self)
		toret.hp = int(self.hp * (hp / 100))
		toret.breakup = toret.breakup.scale(atk / 100)
		toret.atk = int(sum(hit.damage for hit in toret.breakup.hits()))
		return toret
