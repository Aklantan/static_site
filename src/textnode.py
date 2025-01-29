from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag= None, value= text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="strong", value = text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value = text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value = text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value = text_node.text, props = {'href':f'{text_node.url}' })
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value = "", props = {"src": f"{text_node.url}", "alt":f"{text_node.text}"})



class TextNode():
    def __init__ (self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, textnode):
        return self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url

    def __repr__ (self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    