def csv_parse(reader, sep=',', strict=False) -> list[list[int]]:
	rows = []
	for row in reader.read().splitlines():
		rows.append([])
		cells = row.split(sep)
		for cell in cells:
			try:
				rows[-1].append(int(cell))
			except ValueError:
				if strict: continue
				rows[-1].append(cell)
	return rows
