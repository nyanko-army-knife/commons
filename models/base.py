import dataclasses

model_lookup = {}


@dataclasses.dataclass
class Model:
  _klass: str = dataclasses.field(init=False, default="")