import re

from textnode import TextNode, TextType

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
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r" \[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        image_nodes_extracted = extract_markdown_images(old_node.text)

        if not image_nodes_extracted:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text

        for image_node in image_nodes_extracted:
            image_alt = image_node[0]
            image_link = image_node[1]
            sections = current_text.split(f"![{image_alt}]({image_link})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            if len(sections) > 1:
                current_text = sections[1]
            else:
                current_text = ""
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

# def split_nodes_link(old_nodes):
