from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    markdowns = [
        "#### This is a heading",
        "```this is some code```"
    ]
    for markdown in markdowns:
        print(block_to_block_type(markdown))

if __name__=="__main__":
    main()