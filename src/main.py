from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    texts = [
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        "![image](https://i.imgur.com/zjjcJKZ.png)",
        "",
        "This is just a text"
    ]
    for text in texts:
        print(f".\n{split_nodes_image([TextNode(text, TextType.TEXT)])}")

if __name__=="__main__":
    main()