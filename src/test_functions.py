import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import text_node_to_html_node, split_nodes_delimiter

class TestTextToHtml(unittest.TestCase):
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


class TestNodeSplitter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode('This is text with a `code block` word', TextType.TEXT)
        expect = [
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' word', TextType.TEXT),
        ]
        actual = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(expect, actual)
        
    def test_split_no_delim(self):
        node = TextNode('This text has no delimiters', TextType.TEXT)
        expect =[
            TextNode('This text has no delimiters', TextType.TEXT)
        ]
        actual = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(expect, actual)


    def test_split_all_italic(self):
        node = TextNode('_I am all italics_', TextType.TEXT)
        expect = [
            TextNode('I am all italics', TextType.ITALIC),
        ]
        actual = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(expect, actual)


    def test_split_at_end(self):
        node = TextNode('Only **this is bold**', TextType.TEXT)
        expect = [
            TextNode('Only ', TextType.TEXT),
            TextNode('this is bold', TextType.BOLD),
        ]
        actual = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(expect, actual)

    def test_should_error(self):
        node = TextNode('I have _unbalanced delims', TextType.TEXT)
        with self.assertRaisesRegex(Exception, 'unbalanced "_"'):
            split_nodes_delimiter([node], '_', TextType.ITALIC)


        node = TextNode('_More _imbalance_', TextType.TEXT)
        with self.assertRaisesRegex(Exception, 'unbalanced "_"'):
            split_nodes_delimiter([node], '_', TextType.ITALIC)


    def test_mutiple_nodes(self):
        nodes = [
            TextNode('A lot of **bold** items in **this** case', TextType.TEXT),
            TextNode('**so much** is **bold**!', TextType.TEXT),
        ]
        expect = [
            TextNode('A lot of ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' items in ', TextType.TEXT),
            TextNode('this', TextType.BOLD),
            TextNode(' case', TextType.TEXT),
            TextNode('so much', TextType.BOLD),
            TextNode(' is ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode('!', TextType.TEXT),
        ]
        actual = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertEqual(expect, actual)



if __name__ == "__main__":
    unittest.main()