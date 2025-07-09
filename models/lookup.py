import dataclasses
from datetime import datetime
from typing import Any

from commons.models.base import Model

model_lookup = {}
subclasses = []
subclasses_next = [Model]


def setup():
	global subclasses, subclasses_next, model_lookup
	while subclasses_next:
		temp = []
		for _klass in subclasses_next:
			temp.extend(_klass.__subclasses__())
		subclasses.extend(subclasses_next)
		subclasses_next = temp

	for model in subclasses:
		if dataclasses.is_dataclass(model):
			try:
				model_lookup[model.klass()] = model
			except AttributeError:
				pass


def object_hook_ability(dct: dict[str, Any]):
	for k, v in dct.items():
		if isinstance(v, str):
			try:
				dct[k] = datetime.fromisoformat(v)
			except ValueError:
				pass
		else:
			try:
				x = list(map(datetime.fromisoformat, v))
				if len(x): dct[k] = x
			except (TypeError, ValueError):
				pass
	if '_klass' in dct:
		name = dct.pop("_klass")
		return model_lookup[name](**dct)
	return dct
