from enum import Enum


class Trait(str, Enum):
  red = "red"
  floating = "floating"
  black = "black"
  metal = "metal"
  white = "white"
  angel = "angel"
  alien = "alien"
  zombie = "zombie"
  relic = "relic"
  aku = "aku"


class PseudoTrait(str, Enum):
  base = "base"
  witch = "witch"
  eva_angel = "eva angel"
  starred_alien = "starred alien"
  colossus = "colossus"
  behemoth = "behemoth"
  sage = "sage"
