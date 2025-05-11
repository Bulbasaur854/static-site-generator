import unittest
from textnode import *
from inline_markdown import *

class TestSplitNodesDelimiter(unittest.TestCase):        
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class TestExtractMarkdown(unittest.TestCase):  
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images("This is a text without any images")
        self.assertEqual([], matches)

    def test_extract_markdown_images_link(self):
        matches = extract_markdown_images("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links("This is a text without any links")
        self.assertEqual([], matches)  

    def test_extract_markdown_links_image(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual([], matches) 

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_mixed(self):
        node = TextNode("Mixing [a link](https://example.com) with an ![image](https://img.com/abc.png) in one line.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Mixing [a link](https://example.com) with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://img.com/abc.png"),
                TextNode(" in one line.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode("![img1](url1)![img2](url2)![img3](url3)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode("img3", TextType.IMAGE, "url3"),
            ],
            new_nodes,
        )

    def test_split_images_invalid(self):
        node = TextNode("This is not a real image ![not closed properly(url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is not a real image ![not closed properly(url)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt(self):
        node = TextNode("An image with empty alt ![](https://img.com/x.png).", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("An image with empty alt ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://img.com/x.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_special_chars(self):
        node = TextNode("Paragraph with ![first](url1)\n\nthen another ![second](url2) after.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Paragraph with ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode("\n\nthen another ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "url2"),
                TextNode(" after.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![only](url1)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only", TextType.IMAGE, "url1"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode("Check out [Boot.dev](https://www.boot.dev) and [YouTube](https://youtube.com).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("YouTube", TextType.LINK, "https://youtube.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_mixed(self):
        node = TextNode("Mixing [a link](https://example.com) with an ![image](https://img.com/abc.png) in one line.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Mixing ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode(" with an ![image](https://img.com/abc.png) in one line.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode("[first](url1)[second](url2)[third](url3)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "url1"),
                TextNode("second", TextType.LINK, "url2"),
                TextNode("third", TextType.LINK, "url3"),
            ],
            new_nodes,
        )

    def test_split_links_invalid(self):
        node = TextNode("This is not a real link [not closed properly(url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is not a real link [not closed properly(url)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_href(self):
        node = TextNode("An image with empty href [](https://img.com/x.png).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("An image with empty href ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://img.com/x.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is a **bold statement** with an _important_ `code snippet` and a [useful link](https://example.com) plus an ![image alt text](https://example.com/image.jpg) for good measure."
        text_nodes = text_to_textnode(text)
        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold statement", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("important", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code snippet", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("useful link", TextType.LINK, "https://example.com"),
                TextNode(" plus an ", TextType.TEXT),
                TextNode("image alt text", TextType.IMAGE, "https://example.com/image.jpg"),
                TextNode(" for good measure.", TextType.TEXT),
            ],
            text_nodes
        )

    def test_text_to_text_nodes2(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnode(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )

    def test_text_to_text_nodes_order(self):
        text = "This is a `code snippet` with an _important_ **bold statement** and a [useful link](https://example.com) plus an ![image alt text](https://example.com/image.jpg) for good measure."
        text_nodes = text_to_textnode(text)
        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code snippet", TextType.CODE),
                TextNode(" with an ", TextType.TEXT),
                TextNode("important", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("bold statement", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("useful link", TextType.LINK, "https://example.com"),
                TextNode(" plus an ", TextType.TEXT),
                TextNode("image alt text", TextType.IMAGE, "https://example.com/image.jpg"),
                TextNode(" for good measure.", TextType.TEXT),
            ],
            text_nodes
        )

if __name__ == "__main__":
    unittest.main()