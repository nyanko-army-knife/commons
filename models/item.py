from dataclasses import dataclass

from commons.models import Model


@dataclass
class Item(Model):
	_klass = "item"

	id_: int = 0
	name: str = ""
	description: str = ""
	xp_price: int = 0
	stagedrop_id: int = 0
	server_id: int = 0
	src_item_id: int = 0
