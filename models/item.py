from commons.models import Model


class Item(Model):
	id_: int
	name: str
	description: str
	xp_price: int
	stagedrop_id: int
	server_id: int
	src_item_id: int
