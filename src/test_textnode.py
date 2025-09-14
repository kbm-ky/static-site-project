import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a link node", TextType.LINK, 'http://www.yahoo.com/')
        node2 = TextNode("This is a link node", TextType.LINK, 'http://www.yahoo.com/')
        self.assertEqual(node, node2)


    def test_neq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a image node', TextType.IMAGE)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, 'http://someplace.net')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()