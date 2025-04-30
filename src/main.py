from textnode import TextNode, TextType

def main():
    text_node = TextNode("Some anchor text", TextType.LINK, "http://www.bul8a54ur.cum")
    print(text_node)

if __name__=="__main__":
    main()