from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    md = """
This is **bolded** paragraph text in a p tag here

## h2 header
"""

    markdown_to_html_node(md)

if __name__=="__main__":
    main()