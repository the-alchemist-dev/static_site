#!/usr/bin/python3

import unittest
from textnode import TextNode, TextType
from extractnodes import split_nodes_delimiter

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
        nodes = [
            TextNode("This is **bold _text_**", TextType.TEXT),
            TextNode("This is **more `bold` text**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold _text_", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("more `bold` text", TextType.BOLD)
        ]

    def test_split_italic_mult_type(self):
        nodes = [
            TextNode("This is _italic **text**_", TextType.TEXT),
            TextNode("This is _more `italic` text_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic **text**", TextType.ITALIC),
            TextNode("This is ", TextType.TEXT),
            TextNode("more `italic` text", TextType.ITALIC)
        ]

    def test_split_code_mult_type(self):
        nodes = [
            TextNode("This is `**code**`", TextType.TEXT),
            TextNode("This is `_more code_`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("**code**", TextType.CODE),
            TextNode("This is ", TextType.TEXT),
            TextNode("_more code_", TextType.CODE)
        ]

    def test_split_bold_many(self):
        nodes = [
            TextNode("This is **bold** and **this is bold**", TextType.TEXT),
            TextNode("Here is a **bold** word and two more **bold words**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("this is bold", TextType.BOLD),
            TextNode("Here is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and two more ", TextType.TEXT),
            TextNode("bold words", TextType.BOLD)
        ]

    def test_split_italic_many(self):
        nodes = [
            TextNode("This is _italic_ and _this is italic_", TextType.TEXT),
            TextNode("Here is an _italic_ word and two more _italic words_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("this is italic", TextType.ITALIC),
            TextNode("Here is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and two more ", TextType.TEXT),
            TextNode("italic words", TextType.ITALIC)
        ]

    def test_split_code_many(self):
        nodes = [
            TextNode("This is `code` and `this is code`", TextType.TEXT),
            TextNode("Here is `more code` and `even more code`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("this is code", TextType.CODE),
            TextNode("Here is ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("even more code", TextType.CODE)
        ]

    def test_split_not_text_nodes(self):
        nodes = [
            TextNode("**Bold text**", TextType.BOLD),
            TextNode("**Italic text**", TextType.ITALIC),
            TextNode("**Code**", TextType.CODE)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("**Bold text**", TextType.BOLD, None),
            TextNode("**Italic text**", TextType.ITALIC, None),
            TextNode("**Code**", TextType.CODE, None)
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
                TextNode("This is **more bold text**", TextType.TEXT)
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
