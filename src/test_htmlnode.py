import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expect = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        actual =  node.to_html()
        self.assertEqual(expect, actual)

if __name__ == "__main__":
    unittest.main()