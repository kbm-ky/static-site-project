import unittest

from htmlnode import HtmlNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        node = HtmlNode('a', 'yahoo', None, {'href': 'http://www.yahoo.com', 'target': '_blank'})
        expect = ' href="http://www.yahoo.com" target="_blank"'
        actual = node.props_to_html()
        self.assertEqual(expect, actual)

        node = HtmlNode()
        expect = ''
        actual = node.props_to_html()
        self.assertEqual(expect, actual)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode('p', 'Hello, world!')
        expect = '<p>Hello, world!</p>'
        actual = node.to_html()
        self.assertEqual(expect, actual)

        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expect = '<a href="https://www.google.com">Click me!</a>'
        actual = node.to_html()
        self.assertEqual(expect, actual)



if __name__ == "__main__":
    unittest.main()