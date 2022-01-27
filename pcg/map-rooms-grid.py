#!/usr/bin/env python

from enum import Enum

import numpy as np


class Tiles(str, Enum):
    FLOOR = '.'
    WALL = 'w'
    PLAYER = 'P'


class Map:
    def __init__(self, room_width=8, room_height=8, wall_width=1,
                 num_rooms_horizontal=2, num_rooms_vertical=2):
        """ All dimensions in numbers of cells """

        # Dimensions of individual rooms
        self.room_width = room_width
        self.room_height = room_height

        # Width of walls
        self.wall_width = wall_width

        # Number of rooms
        self.num_rooms_horizontal = num_rooms_horizontal
        self.num_rooms_vertical = num_rooms_vertical

        # Calculate total dimensions
        # Total cells minus walls between rooms
        self.map_width = (self.num_rooms_horizontal * self.room_width -
                          (self.num_rooms_horizontal-1) * self.wall_width)
        self.map_height = (self.num_rooms_vertical * self.room_height -
                           (self.num_rooms_vertical-1) * self.wall_width)

    def build(self):
        # Build map
        self.map = np.full((self.map_height, self.map_width),  # Dimensions
                           f"{Tiles.FLOOR}",  # Fill value
                           dtype=np.str_)

        # Draw outer walls
        self.map[0:self.wall_width, :] = f"{Tiles.WALL}"  # Top
        self.map[(self.map_height-self.wall_width):self.map_height, :] = f"{Tiles.WALL}"  # Bottom
        self.map[:, 0:self.wall_width] = f"{Tiles.WALL}"  # Left
        self.map[:, (self.map_width-self.wall_width):self.map_width] = f"{Tiles.WALL}"  # Right

        # Draw walls between rooms
        for i in range(1, self.num_rooms_vertical):  # Horizontal dividers
            a = i * (self.room_height - self.wall_width)
            b = a + self.wall_width
            self.map[a:b, :] = f"{Tiles.WALL}"
        for i in range(1, self.num_rooms_horizontal):  # Vertical dividers
            a = i * (self.room_width - self.wall_width)
            b = a + self.wall_width
            self.map[:, a:b] = f"{Tiles.WALL}"

        return self.map

    def get_map(self):
        output = ""
        height, width = self.map.shape
        for i in range(height):
            for j in range(width):
                output += f"{self.map[i, j]}"
                if j < width-1:
                    output += " "  # Add space between cells
            if i < height-1:
                output += "\n"  # Add break between lines
        return output

    def __repr__(self):
        return self.get_map()


if __name__ == "__main__":
    world = Map(
        room_width=8,
        room_height=8,
        wall_width=1,
        num_rooms_horizontal=2,
        num_rooms_vertical=2
    )
    world.build()
    print(world)
