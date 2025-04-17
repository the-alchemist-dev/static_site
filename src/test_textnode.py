#!/usr/bin/python3

import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This node is one thing", TextType.BOLD)
        node2 = TextNode("This node is another", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_none(self):
        node = TextNode("This is some text", TextType.NORMAL, "https://www.boot.dev")
        node2 = TextNode("This is some text", TextType.NORMAL, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is some text", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is some text", TextType.ITALIC, "https://www.boot.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
