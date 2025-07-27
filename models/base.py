import re

import msgspec


def to_camelcase(x: str) -> str:
	return re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower()


class Model(msgspec.Struct, tag=to_camelcase, tag_field="_klass"):
	pass
