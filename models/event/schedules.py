from datetime import datetime
from typing import TypeAlias, TypeVar

from commons.models import Model

T = TypeVar('T')
Version: TypeAlias = tuple[int, int, int]
Span: TypeAlias = tuple[T, T]

def datespan(span: Span[datetime]) -> str:
	return f"[{span[0].strftime("%Y-%m-%d")}~{span[1].strftime("%Y-%m-%d")}]"


class GachaSchedule(Model):
	_klass = "gacha_schedule"

	time_span: Span[datetime]
	ver_span: Span[Version]
	category: int
	banner_id: int
	slot: int
	roll_cost: int
	roll_rates: tuple[int, int, int, int, int]
	roll_guarantees: tuple[bool, bool, bool, bool, bool]
	modifier: int
	item_drop: int
	message: str

	@property
	def gacha_id(self) -> str:
		return f"{'NREE'[self.category]}{self.banner_id:03}"

	@property
	def modifiers(self) -> list[str]:
		if not self.gacha_id.startswith("R"): return []
		modifiers = []
		if self.modifier & 0b0100:
			modifiers.append("S")  # step up
		if self.modifier & 0b1000:
			modifiers.append(f"I{(self.modifier & 0b0011_1111_1111_0000) >> 3}")  # step up
		if self.modifier & 0b0100_0000_0000_0000:
			modifiers.append("P")  # platinum shard
		if self.roll_rates[-2] > 5000:
			modifiers.append("U")  # double uber rate
		if self.roll_guarantees[-2]:
			modifiers.append("G")  # guaranteed uber
		return modifiers



class ItemSchedule(Model):
	_klass = "item_schedule"

	time_span: Span[datetime]
	ver_span: Span[Version]
	locked_to_dates: list[int]
	event_id: int
	item_id: int
	item_qty: int
	unlock: int
	message: str




class PonosCron(Model):
	_klass = "ponoscron"
	yearly_schedules: list[Span[str]]
	monthly_schedules: list[int]
	weekly_schedules: int # bitmask
	daily_schedules: list[Span[str]]


class SaleSchedule(Model):
	_klass = "sale_schedule"

	time_span: Span[datetime]
	ver_span: Span[Version]
	active_on: list[PonosCron]
	events: list[int]
