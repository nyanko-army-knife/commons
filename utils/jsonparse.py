import dataclasses
import json


class DataEncoder(json.JSONEncoder):
	def default(self, o):
		if dataclasses.is_dataclass(o):
			return dataclasses.asdict(o)
		return super().default(o)
