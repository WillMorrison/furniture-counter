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

    def count_chairs(self, room: Room) -> collections.Counter:
        chair_count = collections.Counter({'W':0, 'P':0, 'S':0, 'C':0})

        # Breadth first search the whole room for chairs.
        visited = set()  # holds coordinates of grid points that have already been visited
        to_visit = collections.deque([(room.row, room.col)])  # hold coordinates of grid points yet to visit

        def visit(row, col):
            if (row, col) in visited:
                return
            visited.add((row, col))

            # update counter if we're visiting a chair
            char = self.grid[row][col]
            if char in CHAIRS:
                chair_count[char] += 1
            
            for next_row, next_col in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)]:
                # avoid revisiting the same coordinates
                if (next_row, next_col) in visited:
                    continue
                # avoid walls and the edges of the grid
                if next_row < 0 or next_col < 0:
                    continue
                try:
                    if self.grid[next_row][next_col] in WALLS:
                        continue
                except IndexError:
                    continue

                # If checks pass, add the adjacent coordinates to the visiting queue
                to_visit.appendleft((next_row, next_col))
        
        while to_visit:
            next_row, next_col = to_visit.pop()
            visit(next_row, next_col)
        
        return chair_count




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='path to file containing room layout')
    args = parser.parse_args()

    with open(args.file, 'rt') as f:
       layout = Layout.from_multiline_string(f.read())