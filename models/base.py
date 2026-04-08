import re
from string.templatelib import Template
from typing import Self

import msgspec

from commons.utils.msg import Msg


def to_camelcase(x: str) -> str:
	return re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower()


class Duration(int, Msg[int]):
	def enc(self) -> int:
		return int(self)

	@classmethod
	def dec(cls, i: int) -> Self:
		return Duration(i)

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
