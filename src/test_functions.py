import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import text_node_to_html_node

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode('This is a bold node', TextType.BOLD)
        expect = f'<b>This is a bold node</b>'
        actual = text_node_to_html_node(node).to_html()
        self.assertEqual(expect, actual)

    def test_italic(self):
        node = TextNode('This is an italic node', TextType.ITALIC)
        expect = f'<i>This is an italic node</i>'
        actual = text_node_to_html_node(node).to_html()
        self.assertEqual(expect, actual)

    def test_code(self):
        node = TextNode('This is a code node', TextType.CODE)
        expect = f'<code>This is a code node</code>'
        actual = text_node_to_html_node(node).to_html()
        self.assertEqual(expect, actual)

    def test_link(self):
        node = TextNode('This is a link node', TextType.LINK, 'http://www.google.com')
        expect = f'<a href="http://www.google.com">This is a link node</a>'
        actual = text_node_to_html_node(node).to_html()
        self.assertEqual(expect, actual)

    def test_image(self):
        node = TextNode('This is an image node', TextType.IMAGE, '/path/to/image.png')
        expect = f'<img src="/path/to/image.png" alt="This is an image node">'
        actual = text_node_to_html_node(node).to_html()
        self.assertEqual(expect, actual)

if __name__ == "__main__":
    unittest.main()