from htmlnode import *
from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter,text_type):
    new_nodes = []     
        
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception ("Not valid markdown syntax")
        else:
          split_text = node.text.split(delimiter)
          for i in range(0,len(split_text),1):
            if split_text[i]:
                if i == 0 or i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i],TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i],text_type))
    
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []     
   
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        split_text = node.text.split(f"![{images[0][0]}]({images[0][1]})")
        if split_text[0] == "":
            pass
        else: 
            new_nodes.append(TextNode(split_text[0],TextType.TEXT))
        new_nodes.append(TextNode(images[0][0],TextType.IMAGE,images[0][1]))
        if split_text[1] != "":
            images = extract_markdown_images(split_text[1])
            # Create a new TextNode with the remaining text
            remaining_node = TextNode(split_text[1], TextType.TEXT)
            # Process it for more images
            if len(images) == 0:
                new_nodes.append(remaining_node)
            else:
                new_nodes.extend(split_nodes_image([remaining_node]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []     
   
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        split_text = node.text.split(f"[{links[0][0]}]({links[0][1]})")
        if split_text[0] == "":
            pass
        else: 
            new_nodes.append(TextNode(split_text[0],TextType.TEXT))
        new_nodes.append(TextNode(links[0][0],TextType.LINK,links[0][1]))
        if split_text[1] != "":
            links = extract_markdown_links(split_text[1])
            # Create a new TextNode with the remaining text
            remaining_node = TextNode(split_text[1], TextType.TEXT)
            if len(links) == 0:
                new_nodes.append(remaining_node)
        
                # Process it for more images
            else:
                new_nodes.extend(split_nodes_link([remaining_node]))  
    return new_nodes      
        
            





def extract_markdown_images(text):
    validate_no_nested_brackets(text)
    validate_no_nested_parentheses(text)
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

    
def extract_markdown_links(text):
    validate_no_nested_brackets(text)
    validate_no_nested_parentheses(text)
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def validate_no_nested_brackets(text):
    bracket_depth = 0
    for char in text:
        if char == "[":
            bracket_depth += 1
            if bracket_depth > 1:  # We've nested brackets
                raise ValueError("Unable to handle nested brackets.")
        elif char == "]":
            bracket_depth -= 1
    if bracket_depth != 0:
        raise ValueError("Unmatched brackets detected.")  # For dangling brackets


def validate_no_nested_parentheses(text):
    paren_depth = 0
    for char in text:
        if char == "(":
            paren_depth += 1
            if paren_depth > 1:  # We've nested parentheses
                raise ValueError("Unable to handle nested parentheses in URL.")
        elif char == ")":
            paren_depth -= 1
    if paren_depth != 0:
        raise ValueError("Unmatched parentheses detected.")  # For dangling parentheses


def text_to_textnodes(text):
    delimit_list =[("**",TextType.BOLD),("*",TextType.ITALIC),("`",TextType.CODE),]
    new_nodes = [TextNode(text,TextType.TEXT)]
    for delim, txttype in delimit_list:
        new_nodes = split_nodes_delimiter(new_nodes,delim,txttype)

    
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    result = []
    for block in blocks:
        lines_unprepped = block.split("\n")
        lines_prepped = []
        for line in lines_unprepped:
            lines_prepped.append(line.strip())
        cleaned_block = "\n".join(lines_prepped)
             
        if cleaned_block:
            result.append(cleaned_block)
        
    return result


def block_to_block_type(block):
    if re.search("^#{1,6}\s.+$",block):
        block_type = "heading"
    elif re.search("```.*```",block):
        block_type = "code"
    elif re.search("^>",block):
        block_type = "quote"
    elif re.search("^-/*\s",block):
        block_type = "unordered_list"
    elif re.search ("^[0-9]\.\s",block):
        block_type = "ordered_list"
    else:
        block_type = "paragraph"

    return block_type
        
