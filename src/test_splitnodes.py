#!/usr/bin/python3

import unittest
from splitnodes import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_split_bold(self):
        nodes = [
            TextNode("This is **bold text**", TextType.TEXT),
            TextNode("This is **more bold text**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("more bold text", TextType.BOLD)
        ]
        

    def test_split_italic(self):
        nodes = [
            TextNode("This is _italic text_", TextType.TEXT),
            TextNode("This is _more italic text_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("This is ", TextType.TEXT),
            TextNode("more italic text", TextType.ITALIC)
        ]

    def test_split_code(self):
        nodes = [
            TextNode("This is `code`", TextType.TEXT),
            TextNode("This is `more code`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("This is ", TextType.TEXT),
            TextNode("more code", TextType.CODE)
        ]

    def test_split_bold_mult_type(self):
        nodes= [
            TextNode("This is **bold _text_**", TextType.TEXT),
            TextNode("This is **more _bold_ text**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold _text_", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("more _bold_ text", TextType.BOLD)
        ]

    def test_split_italic_mult_type(self):
        nodes= [
            TextNode("", TextType.TEXT),
            TextNode("", TextType.TEXT)
        ]

    def test_split_code_mult_type(self):
        nodes= [
            TextNode("", TextType.TEXT),
            TextNode("", TextType.TEXT)
        ]

    def test_split_bold_many(self):
        nodes= [
            TextNode("", TextType.TEXT),
            TextNode("", TextType.TEXT)
        ]

    def test_split_italic_many(self):
        nodes= [
            TextNode("", TextType.TEXT),
            TextNode("", TextType.TEXT)
        ]

    def test_split_code_many(self):
        nodes= [
            TextNode("", TextType.TEXT),
            TextNode("", TextType.TEXT)
        ]

    def test_split_bad_delimiter(self):
        try:
            nodes = [
                TextNode("This is **bold text**", TextType.TEXT),
                TextNode("This is **more normal text**", TextType.TEXT)
            ]
            new_nodes = split_nodes_delimiter(nodes, "@", TextType.BOLD)
        except ValueError:
            assert True
        except Exception as e:
            assert False, f"split_nodes_delimiter() raise {type(e).__name__} instead of ValueError"

    def test_split_no_delimiter(self):
        try:
            nodes = [
                TextNode("This is **bold text**", TextType.TEXT),
                TextNode("This is **more normal text**", TextType.TEXT)
            ]
            new_nodes = split_nodes_delimiter(nodes, "", TextType.BOLD)
        except ValueError:
            assert True
        except Exception as e:
            assert False, f"split_nodes_delimiter() raise {type(e).__name__} instead of ValueError"

    def test_split_wrong_type(self):
        try:
            nodes = [
                TextNode("This is **bold text**", TextType.TEXT),
                TextNode("This is **more normal text**", TextType.TEXT)
            ]
            new_nodes = split_nodes_delimiter(nodes, "**", TextType.TEXT)
        except ValueError:
            assert True
        except Exception as e:
            assert False, f"split_nodes_delimiter() raise {type(e).__name__} instead of ValueError"
