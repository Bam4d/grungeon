#!/usr/bin/env python

from enum import Enum

import numpy as np

""" SETTINGS """
""" All dimensions in number of cells """

# Dimensions of individual rooms
ROOM_WIDTH = 8
ROOM_HEIGHT = 8

# Width of walls
WALL_WIDTH = 1

# Number of rooms
ROOMS_HORIZONTAL = 2
ROOMS_VERTICAL = 2

""" END OF SETTINGS """


class Tiles(str, Enum):
    FLOOR = ' '
    WALL = 'W'
    PLAYER = 'P'


# Calculate total dimensions
# Total cells minus walls between rooms
TOTAL_WIDTH = ROOMS_HORIZONTAL * ROOM_WIDTH - (ROOMS_HORIZONTAL-1) * WALL_WIDTH
TOTAL_HEIGHT = ROOMS_VERTICAL * ROOM_HEIGHT - (ROOMS_VERTICAL-1) * WALL_WIDTH

# Build world
world = np.full((TOTAL_HEIGHT, TOTAL_WIDTH), f"{Tiles.FLOOR}",
                dtype=np.str_)

# Draw walls
# Outer walls
world[0:WALL_WIDTH, :] = f"{Tiles.WALL}"   # Top
world[(TOTAL_HEIGHT-WALL_WIDTH):TOTAL_HEIGHT, :] = f"{Tiles.WALL}"  # Bottom
world[:, 0:WALL_WIDTH] = f"{Tiles.WALL}"   # Left
world[:, (TOTAL_WIDTH-WALL_WIDTH):TOTAL_WIDTH] = f"{Tiles.WALL}"  # Right
# Between rooms
for i in range(1, ROOMS_VERTICAL):  # Horizontal dividers
    a = i * (ROOM_HEIGHT - WALL_WIDTH)
    b = a + WALL_WIDTH
    world[a:b, :] = f"{Tiles.WALL}"
for i in range(1, ROOMS_HORIZONTAL):  # Vertical dividers
    a = i * (ROOM_WIDTH - WALL_WIDTH)
    b = a + WALL_WIDTH
    world[:, a:b] = f"{Tiles.WALL}"

print(world)
