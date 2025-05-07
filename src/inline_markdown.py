# This file contains:
# -------------------
# `BlockType` enum
# `split_nodes_image(old_nodes)`                            - given a list of strings, for each, split the string with images as delimiters 
# `split_nodes_link(old_nodes)`                             - given a list of strings, for each, split the string with links as delimiters
# `text_to_text_node(text)`                                 - convert the given string to a list of text nodes with the corresponding text type
# `makrkdown_to_blocks(markdown)`                           - given markdown whole text as string, return a list of blocks (each one removes empty chars as well)
# `block_to_block_type(markdown_block)`                     - given a amrkdown block string, return its block type

import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading" 
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "u_list"
    O_LIST = "o_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown: formatted section not closed!")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
                
        new_nodes.extend(split_nodes)
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    return split_nodes_image_link(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_image_link(old_nodes, extract_markdown_links, TextType.LINK)

def split_nodes_image_link(old_nodes, extract_markdown_function, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        nodes_extracted = extract_markdown_function(old_node.text)

        if not nodes_extracted:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text

        for node in nodes_extracted:
            text = node[0]
            url = node[1]

            if text_type == TextType.IMAGE:
                sections = current_text.split(f"![{text}]({url})", 1)
            elif text_type == TextType.LINK:
                sections = current_text.split(f"[{text}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(text, text_type, url))

            if len(sections) > 1:
                current_text = sections[1]
            else:
                current_text = ""
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnode(text):
    new_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    
    return new_nodes

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    for node in split_markdown:
        if node == "":
            split_markdown.remove(node)
    return list(map(lambda node: node.strip(), split_markdown))

def block_to_block_type(markdown_block):
    if markdown_block.startswith(("#", "##", "###", "####", "#####", "######")):
        text = markdown_block.lstrip("#")
        if text[0] == " " and len(text) > 1:
            return BlockType.HEADING
    
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    if markdown_block[0] == ">":
        split_block = markdown_block.split("\n")
        is_all_quotes = True
        for node in split_block:
            if node[0] == ">":
                continue
            is_all_quotes = False
        if is_all_quotes:
            return BlockType.QUOTE

    if markdown_block.startswith("- "):
        split_block = markdown_block.split("\n")
        is_all_u_list = True
        for node in split_block:
            if node.startswith("- "):
                continue
            is_all_u_list = False
        if is_all_u_list:
            return BlockType.U_LIST
        
    if markdown_block.startswith("1. "):
        split_block = markdown_block.split("\n")
        is_all_o_list = True
        i = 2
        for node in split_block[1:]:
            if node.startswith(f"{i}. "):
                i += 1
                continue
            is_all_o_list = False
        if is_all_o_list:
            return BlockType.O_LIST
    
    return BlockType.PARAGRAPH