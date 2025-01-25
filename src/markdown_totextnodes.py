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
    if re.search(r"^#{1,6}\s.+$",block):
        block_type = "heading"

    elif block.startswith("```"):  # Check if the block starts as a code block
        block_split = block.splitlines()
        if len(block_split) < 2 or not block_split[-1] != "```":  # Check for closing backticks
            block_type = "paragraph"
        else:
            block_type = "code"


    elif re.search("^>",block):
        block_type = "quote"

    elif re.search(r"(?m)^[-*]\s", block):
        block_type = "unordered_list"
        for line in block.splitlines():
        # Skip completely empty lines within the block
            if line.strip() == "":
                continue
            if not re.match(r"^[-*]\s", line):
                block_type = "paragraph"
                break

        
    elif block.startswith("1. "):
        lines = block.splitlines()
        block_type = "ordered_list"
        for i in range(len(lines)):
        # Skip completely empty lines within the block
            if lines[i].strip() == "":
                continue
            if not lines[i].startswith(f"{i+1}. "):
                block_type = "paragraph"
                break

            
    else:
        block_type = "paragraph"

    return block_type
        


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                heading_type = get_heading_type(block)
                heading_text = block.split(" ",1)[1]
                heading_nodes = text_to_textnodes(heading_text)
                html_nodes.append(ParentNode(heading_type,children=heading_nodes))
                

            case "code":
                code_node = LeafNode("code",block)
                html_nodes.append(ParentNode("pre",children=[code_node]))

            case "quote":
                html_nodes.append(LeafNode("blockquote",block))

            case "unordered_list":
                list_nodes = []
                item_lists = block.split("\n")
                for item in item_lists:
                    item_text = item.lstrip("-* ").strip()
                    item_nodes = text_to_textnodes(item_text)
                    list_nodes.append(ParentNode("li", children=item_nodes))
                html_nodes.append(ParentNode("ul",list_nodes))

            case "ordered_list":
                list_nodes = []
                item_lists = block.split("\n")
                for item in item_lists:
                    item_text = item.lstrip("0123456789. ").strip()
                    item_nodes = text_to_textnodes(item)
                    list_nodes.append(ParentNode("li", children=item_nodes))
                html_nodes.append(ParentNode("ol",list_nodes))

            case "paragraph":
                paragraph_nodes = text_to_textnodes(block)
                html_nodes.append(ParentNode("p",children=paragraph_nodes))
    
    return ParentNode("div",children=html_nodes)


def get_heading_type(text):
    heading_type = f"h{len(re.match("#*", text).group())}"
    return heading_type
  

def create_list_blocks(block,block_type):
    list_nodes = []
    for line in block.splitlines():
        if line.strip():  # Only process non-blank lines
        # Remove list markers (e.g., "-", "*", or "1. ") and any extra spaces
            item_text = line.lstrip("-*0123456789. ").strip()
        
        # Convert the text into inline child nodes (e.g., for bold or italic)
            item_child_nodes = text_to_children(item_text)
        
        # Create a <li> node with the inline child nodes
            list_node = HTMLNode("li", children=item_child_nodes)
            list_nodes.append(list_node)

# Determine the parent list type and wrap the items
    if block_type == "unordered_list":
        list_parent = HTMLNode("ul", children=list_nodes)
    elif block_type == "ordered_list":
       list_parent = HTMLNode("ol", children=list_nodes)

# Return the outer parent list node
    return list_parent


