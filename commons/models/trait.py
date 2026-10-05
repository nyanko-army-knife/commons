from enum import Flag


class Traits(Flag):
	Red = 1 << 0
	Floating = 1 << 1
	Dark = 1 << 2
	Metal = 1 << 3
	Angel = 1 << 4
	Alien = 1 << 5
	Zombie = 1 << 6
	Relic = 1 << 7
	White = 1 << 8
	Aku = 1 << 11


class PseudoTraits(Flag):
	Witch = 1 << 0
	EvaAngel = 1 << 1
	Behemoth = 1 << 2
	Sage = 1 << 3
	Colossus = 1 << 4
	Sentai = 1 << 5
