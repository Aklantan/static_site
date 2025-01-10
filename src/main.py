from textnode import *

def main():
    textnode = TextNode("Thisis a text node",TextType.BOLD,"https://www.boot.dev")
    print(textnode.__repr__())

main()