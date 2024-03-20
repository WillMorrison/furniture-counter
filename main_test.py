import textwrap
import unittest
from main import Layout, Room

class LayoutTest(unittest.TestCase):

    def test_find_rooms(self):
        layout_str = textwrap.dedent("""\
            +-------+-------+
            | (foo) | (bar) |
            |       |       |
            +-------+       |
            |       +-------|
            | (baz quux)    |
            |               |
            +-------+-------+""")
        
        layout:Layout = Layout.from_multiline_string(layout_str)
        expected = [
            Room(name='foo', row=1, col=3),
            Room(name='bar', row=1, col=11),
            Room(name='baz quux', row=5, col=3)
            ]
        self.assertCountEqual(layout.find_rooms(), expected)


if __name__ == '__main__':
    unittest.main()