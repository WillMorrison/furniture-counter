#!/usr/bin/python3
import argparse
import collections
import re

# Characters that define the boundaries of rooms.
WALLS=frozenset(r'|-\/+')

# Characters that define furniture
CHAIRS=frozenset('WPSC')

# Regex for finding room labels
NAME_RE=re.compile(r'\(([a-z ]+)\)')


# A room is a type consisting of a name, and the coordinates of the beginning of the label
Room = collections.namedtuple('Room', ['name', 'row', 'col'])

class Layout:
    """Layout represents a room layout"""

    def __init__(self, layout: list[str]):
        self.grid = layout

    @classmethod
    def from_multiline_string(cls, layout:str) -> 'Layout':
        return cls(layout.split('\n'))

    def find_rooms(self)-> list[Room]:
        rooms = []
        for row, line in enumerate(self.grid):
            for label in NAME_RE.finditer(line):
                rooms.append(Room(name=label[1], row=row, col=label.start(1)))
        return rooms




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='path to file containing room layout')
    args = parser.parse_args()

    with open(args.file, 'rt') as f:
       layout = Layout.from_multiline_string(f.read())