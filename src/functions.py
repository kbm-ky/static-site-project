import re

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
            continue

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

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    pattern = r'!\[([^\n\[\]]*)\]\(([^\n\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    pattern = r'(?<!\!)\[([^\n\[\]]*)\]\(([^\n\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        #extract images
        images = extract_markdown_images(text)
        for alt, url in images:
            image = f'![{alt}]({url})'
            image_node = TextNode(alt, TextType.IMAGE, url)
            #split on image
            t = text.split(image, maxsplit=1)
            if len(t) == 2:
                text_node = TextNode(t[0], TextType.TEXT)
                new_nodes.append(text_node)
                new_nodes.append(image_node)
                text = t[1]
            else:
                raise Exception('can I get here?')

        if len(text) > 0:
            new_node = TextNode(text, TextType.TEXT)
            new_nodes.append(new_node)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        #extract links
        links = extract_markdown_links(text)
        for alt, url in links:
            link = f'[{alt}]({url})'
            link_node = TextNode(alt, TextType.LINK, url)
            #split on link
            t = text.split(link, maxsplit=1)
            if len(t) == 2:
                text_node = TextNode(t[0], TextType.TEXT)
                new_nodes.append(text_node)
                new_nodes.append(link_node)
                text = t[1]
            else:
                raise Exception('can I get here?')

        if len(text) > 0:
            new_node = TextNode(text, TextType.TEXT)
            new_nodes.append(new_node)

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT),]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
