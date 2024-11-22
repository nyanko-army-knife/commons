def csv_parse(reader, sep=',') -> list[list[int | str]]:
  rows = []
  for row in reader.read().splitlines():
    rows.append([])
    cells = row.split(sep)
    for cell in cells:
      try:
        rows[-1].append(int(cell))
      except ValueError:
        rows[-1].append(cell)
  return rows
