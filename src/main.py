from textnode import *

def main():
    text_node = TextNode("This is a ` code block` word", TextType.TEXT)
    print("This is a `code block` word")
    print(split_nodes_delimiter([text_node], "`", TextType.CODE))

    text_node2 = TextNode("This is text with a **bolded phrase* in the middle", TextType.TEXT)
    print("This is text with a **bolded phrase** in the middle")
    print(split_nodes_delimiter([text_node2], "**", TextType.BOLD))

if __name__=="__main__":
    main()