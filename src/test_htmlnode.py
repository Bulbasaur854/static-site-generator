import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "This is the value of the node", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

    def test_props_to_html_empty(self):
        node = HTMLNode("a", "This is the value of the node")
        self.assertEqual(node.props_to_html(), "")    

    def test_props_to_html_eq(self):
        node = HTMLNode("a", "This is the value of the node")
        node2 = HTMLNode("a", "This is the value of the node")
        node_props = node.props_to_html()
        node_props2 = node2.props_to_html()
        self.assertEqual(node_props, node_props2)

    def test_repr(self):
        node = HTMLNode("a", "This is the value of the node")
        self.assertEqual(node.__repr__(), "tag: a, value: This is the value of the node, children: None, props: None")

    def test_repr_eq(self):
        node = HTMLNode("a", "This is the value of the node")
        node2 = HTMLNode("p", "This is the value of the node")
        node_props = node.__repr__()
        node_props2 = node2.__repr__()
        self.assertNotEqual(node_props, node_props2)    

if __name__ == "__main__":
    unittest.main()