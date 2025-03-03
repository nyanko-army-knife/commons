from dataclasses import dataclass

from .entity import Entity


@dataclass(kw_only=True)
class Enemy(Entity):
	_klass: str = "enemy"

	id_: int = 0
	drop: int = 0

	def apply_mag(self, hp: int, atk: int = 0) -> 'Enemy':
		atk = hp if atk == 0 else atk
		self.hp *= hp
		self.atk *= atk
		print(hp, atk)
		return self
