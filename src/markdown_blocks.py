from enum import Enum
from textnode import *
from htmlnode import *
from inline_markdown import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading" 
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "u_list"
    O_LIST = "o_list"

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    for node in split_markdown:
        if node == "":
            split_markdown.remove(node)
    return list(map(lambda node: node.strip(), split_markdown))

def block_to_block_type(markdown_block):
    if not markdown_block:
        return
    
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

def markdown_to_html_node(block):
    markdown_blocks = markdown_to_blocks(block)
    block_nodes = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(" ".join(map(str.strip, block.split("\n"))))
                block_nodes.append(ParentNode("p", children))
            case BlockType.HEADING:
                h_lvl = len(block[:block.index(" ")])
                children = text_to_children(block.lstrip("# "))
                block_nodes.append(ParentNode(f"h{h_lvl}", children))
            case BlockType.CODE:
                strip_block = block.lstrip("` \n").rstrip("`")
                text_node = TextNode(strip_block, TextType.CODE)                
                block_nodes.append(ParentNode("pre", [text_node_to_html_node(text_node)]))
            case BlockType.QUOTE:
                children = text_to_children("".join(block.split(">")).strip())
                block_nodes.append(ParentNode("blockquote", children))
            case BlockType.U_LIST:
                split_list = block.split("- ")[1:]
                children = list(map(lambda item: ParentNode("li", text_to_children(item.strip())), split_list))
                block_nodes.append(ParentNode("ul", children))
            case BlockType.O_LIST:
                split_list = block.split("\n")
                children = list(map(lambda item: ParentNode("li", text_to_children(item[item.index(".") + 2:].strip())), split_list))
                block_nodes.append(ParentNode("ol", children))

    return ParentNode("div", block_nodes)

def text_to_children(text):
    return list(map(lambda node: text_node_to_html_node(node), text_to_textnode(text)))