from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})
        case _:
            raise Exception("invalid text node: unrecognized tag!")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        remaining_text = node.text
        while True:
            first_delimiter_index = remaining_text.find(delimiter)
            if first_delimiter_index == -1:
                # no more delimiters found
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                    break

            second_delimiter_index = remaining_text.find(delimiter, first_delimiter_index + len(delimiter))
            if second_delimiter_index == -1:
                raise Exception("invalid markdown: missing closing delimiter")
            
            if first_delimiter_index > 0:
                # there is some content before first delimiter - add text before first delimiter 
                new_nodes.append(TextNode(remaining_text[:first_delimiter_index], TextType.TEXT))

            # add text between the delimiters
            new_nodes.append(TextNode(remaining_text[first_delimiter_index + len(delimiter):second_delimiter_index], text_type))

            # add text after the second delimiter
            remaining_text = remaining_text[second_delimiter_index + len(delimiter):]

    return new_nodes