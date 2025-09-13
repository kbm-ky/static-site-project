from textnode import TextNode, Bender

def main():
    node = TextNode('This is some anchor text', Bender.AIR_BENDER, 'http://www.boot.dev')
    print(node)


if __name__ == '__main__':
    main()