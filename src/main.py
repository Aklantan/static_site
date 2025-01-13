from textnode import *
from htmlnode import *

def main():
    textnode = TextNode("Thisis a text node",TextType.BOLD,"https://www.boot.dev")
    print(textnode.__repr__())

    node = LeafNode("p", "This is a paragraph of text.")
    print(node.to_html())

main()