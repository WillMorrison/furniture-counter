import collections
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
            |       +-------+
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

    def test_count_chairs_empty_room(self):
        layout_str = textwrap.dedent("""\
            +-------+-------+
            | (foo) | (bar) |
            |       |    C  |
            +-------+   P   |
            |       +-------+
            | (baz quux)    |
            |    WW  S      |
            +-------+-------+""")
        
        layout:Layout = Layout.from_multiline_string(layout_str)
        self.assertEqual(layout.count_chairs(Room(name='foo', row=1, col=3)),
                         collections.Counter({'W':0, 'P':0, 'S':0, 'C':0}))

    def test_count_chairs_one_per_type(self):
        layout_str = textwrap.dedent("""\
            +-------+-------+
            | (foo) | (bar) |
            |       |    C  |
            +-------+   P   |
            |       +-------+
            | (baz quux)    |
            |    WW  S      |
            +-------+-------+""")
        
        layout:Layout = Layout.from_multiline_string(layout_str)
        self.assertEqual(layout.count_chairs(Room(name='bar', row=1, col=11)),
                         collections.Counter({'W':0, 'P':1, 'S':0, 'C':1}))

    def test_count_chairs_multiple_per_type(self):
        layout_str = textwrap.dedent("""\
            +-------+-------+
            | (foo) | (bar) |
            |       |    C  |
            +-------+   P   |
            |       +-------+
            | (baz quux)    |
            |    WW  S      |
            +-------+-------+""")
        
        layout:Layout = Layout.from_multiline_string(layout_str)
        self.assertEqual(layout.count_chairs(Room(name='baz quux', row=5, col=3)),
                         collections.Counter({'W':2, 'P':0, 'S':1, 'C':0}))

    def test_count_chairs_unbounded_room(self):
        layout_str = textwrap.dedent("""\
                    +-------+
                    | (bar) |
                    |    C  |
                    |   P   |
            +-----+ +-------+
              (baz quux)    
                 WW  S      
                             """)
        
        layout:Layout = Layout.from_multiline_string(layout_str)
        self.assertEqual(layout.count_chairs(Room(name='baz quux', row=5, col=3)),
                         collections.Counter({'W':2, 'P':0, 'S':1, 'C':0}))


if __name__ == '__main__':
    unittest.main()