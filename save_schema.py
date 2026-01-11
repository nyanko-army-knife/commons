import json

import msgspec

from commons.models import Cat, Gacha, GachaSchedule, Stage
from commons.models.combo import Combo
from commons.models.enemy import Enemy

cs_ = msgspec.json.schema_components([Cat, Enemy, Stage, Gacha, GachaSchedule, Combo])


def downgrade_to_draft7(schema):
	if not isinstance(schema, dict):
		return schema

	# 1. Rename $defs to definitions
	if "$defs" in schema:
		schema["definitions"] = {k: downgrade_to_draft7(v) for k, v in schema["$defs"].items()}
		del schema["$defs"]

	# 2. Convert prefixItems to items (Draft 7 tuple style)
	if "prefixItems" in schema:
		schema["items"] = [downgrade_to_draft7(i) for i in schema["prefixItems"]]
		del schema["prefixItems"]

		# 3. Handle items: false -> additionalItems: false
		# In 2020-12, 'items' keyword after 'prefixItems' handles the 'rest'
		if "items" in schema and isinstance(schema["items"], bool):
			schema["additionalItems"] = schema["items"]
			# If we are in Draft 7 and items is a list (tuple),
			# we keep 'items' as the list and use 'additionalItems' for the rest.
			if isinstance(schema.get("items"), bool):
				del schema["items"]

	# 4. Fix $ref pointers (from $defs to definitions)
	if "$ref" in schema and isinstance(schema["$ref"], str):
		schema["$ref"] = schema["$ref"].replace("#/$defs/", "#/definitions/")

	# 5. FIX NULLABLE / TYPE ARRAYS
	# Handle the "type": [..., null] or anyOf: [null, ...]
	if "type" in schema:
		t = schema["type"]
		if isinstance(t, list):
			# Convert Python None to string "null" and ensure all are strings
			clean_types = ["null" if x is None or x == "null" else x for x in t]
			schema["type"] = clean_types

	# 6. Fix anyOf Nullable (Common in msgspec/pydantic output)
	if "anyOf" in schema:
		# Check for null in the anyOf variants
		has_null = any(
			sub.get("type") == "null" or sub.get("type") is None for sub in schema["anyOf"] if isinstance(sub, dict))

		if has_null:
			non_null_variants = [sub for sub in schema["anyOf"] if sub.get("type") not in ("null", None)]

			if len(non_null_variants) == 1:
				# Simplify anyOf: [T, null]
				variant = non_null_variants[0]
				schema.update(variant)
				# Convert to type array: ["type", "null"]
				if "type" in schema:
					schema["type"] = [schema["type"], "null"]
				del schema["anyOf"]

	# Recursively apply to all other properties
	for k, v in list(schema.items()):
		if isinstance(v, (dict, list)):
			schema[k] = downgrade_to_draft7(v)

	return schema


# Usage
leg = {
	"$schema": "http://json-schema.org/draft-07/schema#",
	"definitions": {
	}
}
for k, v in json.loads(json.dumps(cs_))[1].items():
	leg["definitions"][k] = downgrade_to_draft7(v)

with open(f"commons/schema_draft7.json", "w") as f:
	json.dump(leg, f, indent=2)

#
# with open("commons/schema.json", "w") as f:
# 	json.dump(cs_, f, indent=2)
#
# with open("commons/schema_gacha.json", "wb") as f:
# 	f.write(msgspec.json.encode(msgspec.json.schema(Gacha)))
