from textnode import TextNode, TextType
from htmlnode import HtmlNode, ParentNode, LeafNode


def text_node_to_html_node(text_node: TextNode) -> HtmlNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)

        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})

        case TextType.IMAGE:
            return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})

        case _:
            raise Exception(f'unsupported type: {text_node.text_type.value}')

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        text = node.text
        if text == '':
            raise Exception('how did a text node w/o text get through?')

        while len(text) > 0:
            t = text.split(delimiter, 1)
            if t[0] != '':
                new_node = TextNode(t[0], TextType.TEXT)
                new_nodes.append(new_node)
            if len(t) == 1:
                break
            text = t[1]
            t = text.split(delimiter, 1)
            if len(t) == 1:
                raise Exception(f'unbalanced "{delimiter}": {node.text}')
            new_node = TextNode(t[0], text_type)
            new_nodes.append(new_node)
            text = t[1]

    return new_nodes
