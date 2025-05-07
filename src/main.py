from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    markdown_to_html_node(md)

if __name__=="__main__":
    main()