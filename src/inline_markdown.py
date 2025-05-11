import re
from textnode import *
from htmlnode import *

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

# Helper functions
# ----------------
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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)