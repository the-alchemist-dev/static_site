#!/usr/bin/python3

import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_to_html(self):
		node = HTMLNode()
		try:
			node.to_html()
			assert False, "to_html() did not raise an exception"
		except NotImplementedError:
			assert True
		except Exception as e:
			assert False, f"to_html() raised {type(e).__name__} instead of NotImplementedError"

	def test_props_to_html_single(self):
		node = HTMLNode(props={"href": "https://www.boot.dev"})
		assert node.props_to_html() == ' href="https://www.boot.dev"'
	
	def test_props_to_html_multiple(self):
		node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
		assert node.props_to_html() == ' href="https://www.boot.dev" target="_blank"'

	def test_repr(self):
		node = HTMLNode(tag="h1", value="This is a header")
		assert node.__repr__() == "HTMLNode(h1, This is a header, None, None)"
