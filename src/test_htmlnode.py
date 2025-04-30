import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' class="greeting" href="https://boot.dev"')

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})")

    # Leaf nodes tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_repr(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.__repr__(), "LeafNode(None, Hello, world!, None)")

    # Parent nodes tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_many_children(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("p", "This is p"),
                LeafNode(None, "This is just text, no tag"),
                LeafNode("i", "Italic text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            ]
        )
        self.assertEqual(
            parent_node.to_html(), 
            '<div><p>This is p</p>This is just text, no tag<i>Italic text</i><a href="https://www.google.com">Click me!</a></div>'
        )

    def test_to_html_children_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_parent = ParentNode("span", [grandchild_node])
        parent_node = ParentNode(
            "div",
            [
                LeafNode("p", "This is p"),
                LeafNode(None, "This is just text, no tag"),
                LeafNode("i", "Italic text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
                child_parent
            ]
        )
        self.assertEqual(
            parent_node.to_html(), 
            '<div><p>This is p</p>This is just text, no tag<i>Italic text</i><a href="https://www.google.com">Click me!</a><span><b>grandchild</b></span></div>'
        )

    def test_parent_repr(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("p", "This is p")
            ]
        )
        self.assertEqual(parent_node.__repr__(), 'ParentNode(div, children: [LeafNode(p, This is p, None)], None)')

if __name__ == "__main__":
    unittest.main()