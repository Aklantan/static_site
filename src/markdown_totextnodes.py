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
        # Check if any line in the block starts with * or - after stripping
        if block.strip().startswith(("*", "-")):
            # Handle list block
            lines = block.split('\n')
            cleaned_lines = [line.strip() for line in lines]
            cleaned_block = '\n'.join(cleaned_lines)
        elif "```" in block:
            lines = block.splitlines()
            start_index = None
            end_index = None
            # Find start and end indices of code block
            for i, line in enumerate(lines):
                if line.startswith("```"):
                    if start_index is None:
                        start_index = i
                    else:
                        end_index = i
                        break
            
            if start_index is not None and end_index is not None:
                # Add text before code block if it exists
                if start_index > 0:
                    before_code = '\n'.join(lines[:start_index]).strip()
                    if before_code:
                        result.append(before_code)
                
                # Add code block
                code_block = '\n'.join(lines[start_index:end_index + 1])
                result.append(code_block)
                
                # Add text after code block if it exists
                if end_index < len(lines) - 1:
                    after_code = '\n'.join(lines[end_index + 1:]).strip()
                    if after_code:
                        result.append(after_code)
            continue
                    
        else:
            # Handle non-list block
            cleaned_block = block.strip()
            
        if cleaned_block:
            result.append(cleaned_block)
    
    return result



def block_to_block_type(block):
    if re.search(r"^#{1,6}\s.+$",block):
        block_type = "heading"

    elif block.startswith("```"):  # Check if the block starts as a code block
        block_split = block.splitlines()
        if len(block_split) < 2 or not block_split[-1].endswith("```"):  # Check for closing backticks
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
        
############################## CURRENTLY WIP below this line. ##############################################

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                heading_type = get_heading_type(block)
                heading_text = block.split(" ",1)[1]
                heading_nodes = text_to_children(heading_text)
                html_nodes.append(ParentNode(heading_type,children=heading_nodes))
                

            case "code":
                cleaned_block = clean_code_block(block)
                code_node = LeafNode("code",cleaned_block)
                html_nodes.append(ParentNode("pre",children=[code_node]))

            case "quote":
                cleaned_quote = clean_quote_block(block)
                html_nodes.append(ParentNode("blockquote",text_to_children(cleaned_quote)))

            case "unordered_list" | "ordered_list":

                html_nodes.append(create_list_blocks(block,block_to_block_type(block)))



            case "paragraph":
                paragraph_nodes = text_to_children(block)
                html_nodes.append(ParentNode("p",children=paragraph_nodes))
    
    return ParentNode("div",children=html_nodes)


def get_heading_type(text):
    heading_type = f"h{len(re.match("#*", text).group())}"
    return heading_type

def text_to_children(text):
    new_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        new_nodes.append(text_node_to_html_node(node))

    return new_nodes



def create_list_blocks(block,block_type):
    list_nodes = []
    for line in block.splitlines():
        if line.strip():  # Only process non-blank lines
        # Remove list markers (e.g., "-", "*", or "1. ") and any extra spaces
            item_text = line.lstrip("-*0123456789. ").strip()
        
        # Convert the text into inline child nodes (e.g., for bold or italic)
            item_child_nodes = text_to_children(item_text)
        
        # Create a <li> node with the inline child node
            list_node = ParentNode("li", children=item_child_nodes)
            list_nodes.append(list_node)

# Determine the parent list type and wrap the items
    if block_type == "unordered_list":
        list_parent = ParentNode("ul", children=list_nodes)
    elif block_type == "ordered_list":
       list_parent = ParentNode("ol", children=list_nodes)

# Return the outer parent list node
    return list_parent

def clean_lists(markdown):
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


def clean_code_block(block):
    lines = block.split('\n')
    print(lines)
    # Remove first and last lines (which contain ```)
    lines = lines[1:-1]
    # Join the remaining lines back together
    return "\n".join(lines)



def clean_quote_block(block):
    lines = block.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip("> "))
    return "\n".join(cleaned_lines)


