#!/usr/bin/python3

import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        assert node == node2

    def test_not_eq(self):
        node = TextNode("This node is one thing", TextType.BOLD)
        node2 = TextNode("This node is another", TextType.BOLD)
        assert node != node2

    def test_url_not_none(self):
        node = TextNode("This is some text", TextType.NORMAL, "https://www.boot.dev")
        node2 = TextNode("This is some text", TextType.NORMAL, "https://www.boot.dev")
        assert node == node2
        
    def test_url_not_eq(self):
        node = TextNode("This is some text", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is some text", TextType.ITALIC, "https://www.boot.com")
        assert node != node2

    def test_repr(self):
        node = TextNode("Testing the print func", TextType.BOLD, None)
        assert node.__repr__() == 'TextNode(Testing the print func, TextType.BOLD, None)'


if __name__ == "__main__":
    unittest.main()
