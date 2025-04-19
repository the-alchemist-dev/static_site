#!/usr/bin/python3

import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        assert node.to_html() == "<p>Hello, world!</p>"

    def test__link(self):
        node = LeafNode("a", "This should be a link", props={"href": "https://www.boot.dev"})
        assert node.to_html() == '<a href="https://www.boot.dev">This should be a link</a>'

    def test_link_new_page(self):
        node = LeafNode("a", "Link opens new tab", props={"href": "https://www.boot.dev", "target": "_blank"})
        assert node.to_html() == '<a href="https://www.boot.dev" target="_blank">Link opens new tab</a>'

    def test_raw_text(self):
        node = LeafNode(None, "This is raw text")
        assert node.to_html() == "This is raw text"

    def test_repr(self):
        node = LeafNode("h1", "Header 1")
        assert node.__repr__() == "LeafNode(h1, Header 1, None, None)"
