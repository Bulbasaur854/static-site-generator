import re
from enum import Enum
from textnode import *
from htmlnode import *

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

def split_nodes_image(old_nodes):
    return split_nodes_image_link(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_image_link(old_nodes, extract_markdown_links, TextType.LINK)

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
                # text_node = TextNode(block.strip("`\n"), TextType.CODE)                
                # block_nodes.append(ParentNode("pre", [text_node_to_html_node(text_node)]))
                code_content = "\n".join(map(str.rstrip, block.strip("`\n").split("\n")))
                text_node = TextNode(code_content, TextType.CODE)
                block_nodes.append(ParentNode("pre", [text_node_to_html_node(text_node)]))
            case BlockType.QUOTE:
                children = text_to_children("".join(block.split("> ")))
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
    # for block in block_nodes:
    #     print(f"{block.to_html()}\n----------")

# Helper functions
# ----------------
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

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

def text_to_children(text):
    return list(map(lambda node: text_node_to_html_node(node), text_to_textnode(text)))