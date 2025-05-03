import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK, "http://google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.__repr__(), "TextNode(This is a text node, link, None)")   

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://www.mywebsite.cum")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props_to_html(), ' href="http://www.mywebsite.cum"')
    
    def test_text_to_html_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, "/my/image/location")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), ' src="/my/image/location" alt="This is an image node"')

class TestSplitNodesDelimiter(unittest.TestCase):        
    def test_split_nodes_code(self):
        text_node = TextNode("This is a ` code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([text_node], "`", TextType.CODE),
            [TextNode("This is a " , TextType.TEXT), TextNode(" code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        )

    def test_split_nodes_bold(self):
        text_node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([text_node], "**", TextType.BOLD),
            [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded phrase", TextType.BOLD), TextNode(" in the middle", TextType.TEXT)]
        )

if __name__ == "__main__":
    unittest.main()