from dataclasses import dataclass

from commons.models import Model

SERIES = ["Tales of the Nekoluga", "The Dynamites", "Sengoku Wargods Vajiras", "Galaxy Gals", "Dragon Emperors", "Red Busters",
	 "Ultra Souls", "Dark Heroes", "Halloween Gacha", "Xmas Gals", "Goodbye <year>!", "Yurudrasil Collab",
	 "Metal Slug Defense Collab", "Merc Storia Collab", "Survive! Mola Mola! Collab", "Annihilation City Collab",
	 "Welcome <year>!", "Princess Punt/Merc Storia/Million Arthur/Dragon Poker", "Almighties", "UBERFEST",
	 "Gals of Summer", "Platinum Ticket Banner", "Air Busters", "Puella Magi Madoka Magica Collab", "Iron Legion",
	 "CRASH FEVER Collab", "Easter Carnival", "EPICFEST", "Girls & Monsters", "Gudetama Collab", "Ultra Selection",
	 "Miracle Chance", "Metal Busters", "Elemental Pixies", "Fate/stay Night Collab", "Best of the Best",
	 "PowerPro Baseball Collab", "Evangelion Set 1", "Bikkuriman Collab", "NEO Best of the Best", "Street Fighter Collab",
	 "Excellent Selection", "SUPERFEST", "Hatsune Miku Collab", "Evangelion Set 2", "Wave Busters",
	 "Legend Ticket Banner", "DynastyFest", "Valentine's Gals", "Ranma 1/2 Collab", "RoyalFest",
	 "River City Clash Capsules", "White Day", "June Bride", "Street Fighter Collab Blue Team",
	 "Street Fighter Collab Red Team", "Colossus Busters", "River City Clash Capsules Red Team",
	 "River City Clash Capsules White Team", "BUSTERFEST", "Metal Slug Attack Collab", "90 Million DL Special Capsules",
	 "Tower of Saviors Collab Capsules", "Rurouni Kenshin Collab", "Gals of Summer Sunshine", "Gals of Summer Blue Ocean",
	 "Ultra 4 Selection", "Miracle 4 Selection", "Excellent 4 Selection", "100M DL Celebration",
	 "Best of the Best (Milestone Edition)", "Seasonal GGals Step-Up Banner", "Baki Collab"]

# IDs offset -1
REINFORCEMENTS = {
	"131": "N",
	"445": "GR",
	"239": "R",
}

@dataclass
class Gacha(Model):
	_klass="Gacha"

	id_: int
	category: str
	enabled: bool
	ticket_item_id: int
	series_id: int
	chara_id: int
	units: dict[int, int]
	blue_orbs: dict[int, int]
	items: dict[int, int]

	@property
	def code(self) -> str:
		return f"{self.series_id}{self.id_:03}"

	@property
	def series_name(self) -> str:
		match self.category:
			case "R":
				return SERIES[self.series_id]
			case "N":
				return "Normal Gacha"
			case "E":
				return "Special Gacha idk lmao"
			case _:
				return "how did you get here"

	@property
	def extras(self) -> list[str]:
		if self.category != "R": return []
		toret = []
		for captain, extra in REINFORCEMENTS.items():
			if captain in self.units:
				toret.append(extra)
		return toret
				