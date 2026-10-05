from plum import dispatch
import enum
import re
from string.templatelib import Template
from typing import Self, TypeVar, Any

import msgspec
import serde

from commons.utils.msg import Msg


def to_camelcase(x: str) -> str:
	return re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower()


E = TypeVar("E", bound=enum.Flag)
def deser_flag[E: enum.Flag](cls: type[E], val: str):
	out = cls(0)
	if val is "":
		return out

	tags = val.split(" | ")
	for tag in tags:
		out |= cls[tag]
	return out


def ser_flag[E: enum.Flag](val: E) -> str:
	return val.name.replace('|', ' | ') if val.name else ""


def bitflag_field(cls: type[E]) -> Any:
	return serde.field(serializer=lambda x: ser_flag(x), deserializer=lambda x: deser_flag(cls, x), default=cls(0))

def intenum_field(cls: type[enum.IntEnum]) -> Any:
	return serde.field(
		serializer=lambda x: x.name,
		deserializer=lambda x: cls[x],
		default=0
	)

def strenum_list_field(cls: type[enum.StrEnum]) -> Any:
	return serde.field(
		serializer=lambda xs: [x.name for x in xs],
		deserializer=lambda xs: [cls[x] for x in xs],
		default_factory=list,
	)

def strenum_field(cls: type[enum.StrEnum]) -> Any:
	return serde.field(
		serializer=lambda xs: xs.name,
		deserializer=lambda xs: cls[xs],
		default_factory=cls,
	)


class Duration(int, Msg[int]):
	def enc(self) -> int:
		return int(self)

	def __add__(self, other: Any) -> Duration:
		return Duration(int(self) + int(other))

	def __sub__(self, other: Any) -> Duration:
		return Duration(int(self) - int(other))

	def __floordiv__(self, other: Any) -> Duration:
		return Duration(int(self) // int(other))

	@classmethod
	def dec(cls, val: int) -> Self:
		return cls(val)

	def __format__(self, format_spec: str) -> str:
		if 'f' not in format_spec and 's' not in format_spec:
			format_spec = 'f' if self <= 150 else 's'
		match format_spec:
			case 's':
				return f"{int(self) / 30:.02,f}s"
			case 'f' | _:
				return f"{int(self):,}f"


class Model(msgspec.Struct, tag=to_camelcase, tag_field="_klass"):
	pass

	def text(self) -> Template:
		return t"{str(self)}"
