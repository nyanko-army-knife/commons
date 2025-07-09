import dataclasses
import json
from datetime import datetime


class DataEncoder(json.JSONEncoder):
	def default(self, o):
		if dataclasses.is_dataclass(o):
			return dataclasses.asdict(o)
		if isinstance(o, datetime):
			return o.isoformat()
		return super().default(o)
