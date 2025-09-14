import unittest

from htmlnode import HtmlNode

class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HtmlNode('a', 'yahoo', None, {'href': 'http://www.yahoo.com', 'target': '_blank'})
        expect = ' href="http://www.yahoo.com" target="_blank"'
        actual = node.props_to_html()
        self.assertEqual(expect, actual)

        node = HtmlNode()
        expect = ''
        actual = node.props_to_html()
        self.assertEqual(expect, actual)
        


if __name__ == "__main__":
    unittest.main()