from enum import Enum

# The different types of hexes available on a
# Catan board
class TileType(Enum):
    Desert = 0
    Fields = 1
    Pasture = 2
    Mountains = 3
    Hills = 4
    Forest = 5
WOOD_COLOR = (0,43,0)
WHEAT_COLOR = (211, 181, 29)
BRICK_COLOR = (165, 96, 21)
STONE_COLOR = (139, 236, 244)
SHEEP_COLOR = (40,255,55)
DESERT_COLOR = (0,0,0)