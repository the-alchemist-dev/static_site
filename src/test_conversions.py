#!/usr/bin/python3

import unittest
from textnode import *
from conversions import *

class TestConversions(unittest.TestCase):
    def test_node_conversion_default(self):
        text_node = TextNode("This should be raw text")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "This should be raw text"
        
    def test_node_conversion_normal(self):
        text_node = TextNode("This should be raw text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "This should be raw text"

    def test_node_conversion_bold(self):
        text_node = TextNode("This should be bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "This should be bold text"

    def test_node_conversion_italic(self):
        text_node = TextNode("This should be italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "i"
        assert html_node.value == "This should be italic text"

    def test_node_conversion_code(self):
        text_node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "code"
        assert html_node.value == "print('Hello, world!')"

    def test_node_conversion_link(self):
        text_node = TextNode("This should be a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.value == "This should be a link"
        assert html_node.props == {"href": "https://www.boot.dev"}

    def test_node_conversion_image(self):
        text_node = TextNode("This is image alt text", TextType.IMAGE, "/images/image.png") 
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props == {"src": "/images/image.png", "alt": "This is image alt text"}

if __name__ == "__main__":
    unittest.main()
