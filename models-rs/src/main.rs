use std::{
	env,
	fs::{self, read_to_string},
	path::Path,
};

use typify::import_types;

import_types!("schema_draft7.json");

fn main() {
	let inp = read_to_string("cats.json").unwrap();
	let cats = serde_json::from_str::<Vec<Option<Cat>>>(&inp).unwrap();
	dbg!(&cats[720]);
}
