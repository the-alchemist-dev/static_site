#!/usr/bin/python3

import unittest
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestParentNode(unittest.TestCase):
	def test_to_html_with_children(self):
	    child_node = LeafNode("span", "child")
	    parent_node = ParentNode("div", [child_node])
	    assert parent_node.to_html() == "<div><span>child</span></div>"

	def test_to_html_with_grandchildren(self):
	    grandchild_node = LeafNode("b", "grandchild")
	    child_node = ParentNode("span", [grandchild_node])
	    parent_node = ParentNode("div", [child_node])
	    assert parent_node.to_html() == "<div><span><b>grandchild</b></span></div>"

	def test_to_html_child_no_tag(self):
		parent_node = ParentNode("p", [LeafNode(None, "No tag on me")])
		assert parent_node.to_html() == "<p>No tag on me</p>"

	def test_to_html_deeply_nested(self):
		parent_node = ParentNode(
			"div",
			[
				ParentNode(
					"span",
					[ParentNode("p", [LeafNode("b", "Bold text")])]
				)
			]
		)
		assert parent_node.to_html() == "<div><span><p><b>Bold text</b></p></span></div>"

	def test_to_html_empty_children(self):
		try:
			parent_node = ParentNode("div", [])
			parent_node.to_html()
			assert False, "Expected ValueError, but no exception was raised"
		except ValueError:
			assert True
		except Exception as e:
			assert False, f".to_html() raised {type(e).__name__} instead of ValueError"

	def test_to_html_parent_none_tag(self):
		try:
			parent_node = ParentNode(None, [LeafNode("p", "Just some text")])
			parent_node.to_html()
			assert False, "Expected ValueError, but no exception was raised"
		except ValueError:
			assert True
		except Exception as e:
			assert False, f".to_html() raised {type(e).__name__} instead of ValueError"

	def test_repr(self):
	    parent_node = ParentNode("div", [LeafNode("p", "Text")])
	    assert parent_node.__repr__() == "ParentNode(div, [LeafNode(p, Text, None, None)], None)"
