from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"
    print(markdown_to_blocks(markdown))

if __name__=="__main__":
    main()