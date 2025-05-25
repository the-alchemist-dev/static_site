#!/usr/bin/python3

import unittest
from site_generator.textnode import TextNode
from site_generator.enumerations import TextType
from site_generator.conversions import (
    text_to_textnodes,
    text_node_to_html_node,
    markdown_to_blocks
)

class TestConversions(unittest.TestCase):
    def test_text_node_to_html_node_default(self):
        text_node = TextNode("This should be raw text")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "This should be raw text"

    def test_text_node_to_html_node_normal(self):
        text_node = TextNode("This should be raw text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "This should be raw text"

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This should be bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "This should be bold text"

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("This should be italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "i"
        assert html_node.value == "This should be italic text"

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "code"
        assert html_node.value == "print('Hello, world!')"

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This should be a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.value == "This should be a link"
        assert html_node.props == {"href": "https://www.boot.dev"}

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("This is image alt text", TextType.IMAGE, "/images/image.png")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props == {"src": "/images/image.png", "alt": "This is image alt text"}

    def test_text_node_to_html_node_none_text(self):
        text_node = TextNode(None, TextType.TEXT, None)
        try:
            text_node_to_html_node(text_node)
            assert False, "Should have raised Exception"
        except Exception as e:
            assert "Text value cannot be None" in str(e)

    def test_text_to_textnodes_bold_only(self):
        text = "This is **text** with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev", TextType.TEXT, None)
        ]

    def test_text_to_textnodes_italic_only(self):
        text = "This is text with an _italic_ word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is text with an ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev", TextType.TEXT, None)
        ]

    def test_text_to_textnodes_code_only(self):
        text = "This is text with an italic word and a `code block` and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is text with an italic word and a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev", TextType.TEXT, None)
        ]

    def test_text_to_textnodes_image_only(self):
        text = "This is text with an italic word and a code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is text with an italic word and a code block and an ", TextType.TEXT, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a link https://boot.dev")
        ]

    def test_text_to_textnodes_link_only(self):
        text = "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]

    def test_text_to_textnodes_text_formats(self):
        text = "This is **text** with an _italic_ word and a `code block` and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev", TextType.TEXT, None)
        ]

    def test_text_to_textnodes_image_and_link(self):
        text = "This is text with an italic word and a code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is text with an italic word and a code block and an ", TextType.TEXT, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]

    def test_text_to_textnodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.TEXT, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]

        def test_text_to_textnodes_empty_string(self):
            text = ""
            nodes = text_to_textnodes(text)
            assert nodes == [TextNode("", TextType.TEXT, None)]

        def test_text_to_textnodes_unclosed_bold(self):
            text = "This is **bold"
            nodes = text_to_textnodes(text)
            assert nodes == [TextNode("This is **bold", TextType.TEXT, None)]

        def test_text_to_textnodes_nested_formatting(self):
            text = "**bold and _italic_**"
            nodes = text_to_textnodes(text)
            # Should not parse nested formatting, treat as bold only
            assert nodes == [
                TextNode("bold and _italic_", TextType.BOLD, None)
            ]

    def test_markdown_to_blocks_one_line(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]

    def test_markdown_to_blocks_two_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]

    def test_markdown_to_blocks_no_lines(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items"
        ]

    def test_markdown_to_blocks_many_extra_lines(self):
        md = """



This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items



"""
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n   \n\n   "
        blocks = markdown_to_blocks(md)
        assert blocks == []

    def test_markdown_to_blocks_trailing_leading_newlines(self):
        md = "\n\nFirst block\n\nSecond block\n\n"
        blocks = markdown_to_blocks(md)
        assert blocks == ["First block", "Second block"]

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single block"
        blocks = markdown_to_blocks(md)
        assert blocks == ["Just a single block"]


# this is where tests for block_to_blocktype() will be as soon as it's fully written
# there will be more of them than below -- these are just placeholders for parts that need testing
    def test_block_to_blocktype_header(self):
        pass

    def test_block_to_blocktype_code(self):
        pass

    def test_block_to_blocktype_quote(self):
        pass

    def test_block_to_blocktype_unord_list(self):
        pass

    def test_block_to_blocktype_ord_list(self):
        pass


if __name__ == "__main__":
    unittest.main()
