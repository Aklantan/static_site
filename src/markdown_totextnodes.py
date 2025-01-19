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
        cleaned_block = block.strip()
        if cleaned_block:
            result.append(cleaned_block)
    print(result)
        
    return result




    ############### The below was a previous more complicated iteration
    # list_str =""
    # block_str = ""
    # in_list_block = False
    # in_text_block = False
    # for line in lines:
    #     if line[:1] == "#":
    #         if in_list_block == True:
    #             new_blocks.append(list_str)
    #             in_list_block = False
    #         if in_text_block == True:
    #             new_blocks.append(block_str)
    #             in_text_block = False
    #         new_blocks.append(line)
    #     if line[:1] == "*":
    #         if in_text_block == True:
    #             new_blocks.append(block_str)
    #             in_text_block = False
    #         list_str += f"{line}\n"
    #         in_list_block = True
    #     else:
    #         if in_list_block == True:
    #             new_blocks.append(list_str)
    #             in_list_block = False
    #         block_str += f"{line}\n"
    #         in_text_block = True

    # if in_list_block:
    #         new_blocks.append(list_str)
    #         in_list_block = False
    # if in_text_block:
    #     new_blocks.append(block_str)

            

    
        

        
def test_markdown_to_blocks():
        # Test 1: Basic blocks with single separator
        assert markdown_to_blocks("Block 1\n\nBlock 2") == ["Block 1", "Block 2"]

        # Test 2: Multiple blank lines between blocks
        assert markdown_to_blocks("Block 1\n\n\n\nBlock 2") == ["Block 1", "Block 2"]

        # Test 3: List items (should stay together)
        assert markdown_to_blocks("# Heading\n\n* Item 1\n* Item 2") == ["# Heading", "* Item 1\n* Item 2"]

        # Test 4: Whitespace handling
        assert markdown_to_blocks("  Block 1  \n\n  Block 2  ") == ["Block 1", "Block 2"]

        # Test 5: Complex markdown (like from the example)
        test_md = """# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item"""
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        result = markdown_to_blocks(test_md)
        print("\nExpected:", expected)
        print("Got:", result)
        print("\nExpected[0]:", repr(expected[0]))
        print("Got[0]:", repr(result[0]))
        
        #self.assertEqual(result, expected)

test_markdown_to_blocks()