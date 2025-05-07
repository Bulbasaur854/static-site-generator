from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    markdowns = [
        "#### This is a heading",
        "```this is some code```",
        "> This is quote\n> bla bla bla",
        "- This is an unordered list\n- item\n- another item",
        "1. This is a list\n2. item\n3. another item"
    ]
    for markdown in markdowns:
        print(block_to_block_type(markdown))

if __name__=="__main__":
    main()