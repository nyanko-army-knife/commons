from dataclasses import dataclass, field

from commons.models.base import Model


@dataclass
class Schematic(Model):
	_klass = "schematic"

	enemy_id: int = 0  # offset by +1?
	mag_hp: int = 0
	mag_atk: int = 0
	score: int = 0
	is_boss: bool = False

	quantity: int = 0
	is_start_after_hp: bool = False  # whether or not to apply start delay after hp condition is satisfied
	start: int = 0
	spawn_hp: int = 0
	respawn_min: int = 0
	respawn_max: int = 0
	kill_count: int = 0  # spawn on kill count

	layer_min: int = 0
	layer_max: int = 0

	@property
	def mag_str(self) -> str:
		if self.mag_atk in (0, self.mag_hp):
			return f"{self.mag_hp:,}%"
		else:
			return f"{self.mag_hp:,}%, {self.mag_atk:,}%"

	@property
	def respawn_str(self) -> str:
		if self.respawn_min == self.respawn_max:
			return f"{self.respawn_max:,}f"
		else:
			return f"{self.respawn_min:,}~{self.respawn_max:,}f"

	@property
	def qty_str(self) -> str:
		return "∞" if self.quantity == 0 else f"{self.quantity}"


@dataclass
class Stage(Model):
	_klass = "stage"
	id_: tuple[str, int, int] = None
	name: str = ''

	castle_id: int = 0
	no_continues: bool = False
	ex_chance: int = 0
	ex_map: int = 0
	ex_stage_min: int = 0
	ex_stage_max: int = 0

	length: int = 0
	base_health: int = 0
	enemy_limit: int = 0
	enemy_base_id: int = 0
	global_respawn_min: int = 0
	global_respawn_max: int = 0
	background_id: int = 0
	time_limit: int = 0  # dojo only
	boss_shield: bool = False

	schematics: list[Schematic] = None

	@property
	def id_str(self):
		return f"{self.id_[0]}-{self.id_[1]:03}-{self.id_[2]:02}"


@dataclass
class Map(Model):
	_klass = "map_"
	id_: tuple[str, int] = None
	name: str = ''

	stages: list[Stage] = field(default_factory=list)

	@property
	def id_str(self):
		return f"{self.id_[0]}-{self.id_[1]:03}"


@dataclass
class Category(Model):
	_klass = "category"
	id_: str = ""

	maps: list[Map] = field(default_factory=list)
