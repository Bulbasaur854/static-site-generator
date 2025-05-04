from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    texts = [
        "Check out [Boot.dev](https://www.boot.dev) and [YouTube](https://youtube.com).",
        "Mixing [a link](https://example.com) with an ![image](https://img.com/abc.png) in one line.",
        "![img1](url1)![img2](url2)![img3](url3)",
        "This is not a real image ![not closed properly(url)",
        "An image with empty alt ![](https://img.com/x.png).",
        "Paragraph with ![first](url1)\n\nthen another ![second](url2) after.",
        "![only](url1)"
    ]
    i = 1
    for text in texts:
        print(f"texts[{i}]: {split_nodes_image([TextNode(text, TextType.TEXT)])}")
        if i != len(texts):
            print(f".\n.\n.")
        else:
            print(f".\n.\n.\nFinished processing!")
        i += 1

if __name__=="__main__":
    main()