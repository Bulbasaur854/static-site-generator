import unittest
from markdown_blocks import *

class TestMarkdownToBlocks(unittest.TestCase):        
    def test_markdown_to_blocks(self):
        markdown = "This is **bolded** paragraph\n\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n- This is a list\n- with items"     
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_blocks(self):
        markdown = "This is **bolded** paragraph\n\n\n\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n\n- This is a list\n- with items"     
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_blocktype(self):
        markdown_blocks = [
            "#### This is a heading",
            "```this is some code```",
            "> This is quote\n> bla bla bla",
            "- This is an unordered list\n- item\n- another item",
            "1. This is a list\n2. item\n3. another item"
        ]
        # for block in markdown_blocks:
        block_types = list(map(lambda block: block_to_block_type(block), markdown_blocks))
        self.assertEqual(
            [
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.U_LIST,
                BlockType.O_LIST,
            ]
            ,
            block_types
        )

    def test_block_to_blocktype_invalid(self):
        markdown_blocks = [
            "####/ This is a heading",
            "``this is some code```",
            "> This is quote\nbla bla bla",
            "- This is an unordered list\n-item  \n- another item",
            "1. This is a list\n4. item\n3. another item"
        ]
        # for block in markdown_blocks:
        block_types = list(map(lambda block: block_to_block_type(block), markdown_blocks))
        self.assertEqual(
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
            ,
            block_types
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = "This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = "# Header 1\n\n## Header 2\n\n##### Header 5"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header 1</h1><h2>Header 2</h2><h5>Header 5</h5></div>"
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = "> Quote of the day:\n> monkeys love gambling\n> Thanks everyone"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote of the day:\nmonkeys love gambling\nThanks everyone</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- banana\n- milk\n- eggs"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>banana</li><li>milk</li><li>eggs</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )