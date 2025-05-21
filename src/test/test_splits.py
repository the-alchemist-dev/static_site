#!/usr/bin/python3

import unittest
from site_generator.textnode import TextNode
from site_generator.enumerations import TextType
from site_generator.splits import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    extract_markdown_images,
    extract_markdown_links
)

class TestSplitNodes(unittest.TestCase):

    def test_split_no_formats(self):
        nodes = [
            TextNode("This is actually just text", TextType.TEXT),
            TextNode("This is also just text", TextType.TEXT)
        ]
        #delimiter and text_type don't actually matter here, just need for function call
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is actually just text", TextType.TEXT),
            TextNode("This is also just text", TextType.TEXT)
        ]

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

    def test_split_images_text_at_end(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and more", TextType.TEXT, None)
        ]

    def test_split_images_no_text_at_end(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

    def test_split_images_no_text_or_space_between(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and more", TextType.TEXT, None)
        ]

    def test_split_images_no_text_except_space(self):
        nodes = [
            TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" ", TextType.TEXT, None),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

    def test_split_images_no_text_no_space(self):
        nodes = [
            TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

    def test_split_images_wrong_text_type(self):
        try:
            nodes = [
                TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT)
            ]
            new_nodes = split_nodes_images(nodes, TextType.BOLD)
        except ValueError:
            assert True
        except Exception as e:
            assert False, f"split_nodes_images() raise {type(e).__name__} instead of ValueError"

    def test_split_images_text_type_image(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.IMAGE)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.IMAGE, None)
        ]

    def test_split_images_default_text_type(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT, None),
			TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
			TextNode(" and ", TextType.TEXT, None),
			TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and more", TextType.TEXT, None)
        ]

    def test_split_images_no_images(self):
        nodes = [
            TextNode("This is text with a rick roll https://i.imgur.com/aKaOqIh.gif and obi wan https://i.imgur.com/fJRm4Vk.jpeg and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("This is text with a rick roll https://i.imgur.com/aKaOqIh.gif and obi wan https://i.imgur.com/fJRm4Vk.jpeg and more", TextType.TEXT, None)
        ]

    def test_split_images_bad_image_syntax(self):
        nodes = [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif and ![obi wanhttps://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(nodes, TextType.IMAGE)
        assert new_nodes == [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif and ![obi wanhttps://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT, None)
        ]

    def test_split_links_text_at_end(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
			TextNode("This is text with a link ", TextType.TEXT, None),
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" and ", TextType.TEXT, None),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
			TextNode(" and more", TextType.TEXT, None)
        ]

    def test_split_links_no_text_at_end(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
			TextNode("This is text with a link ", TextType.TEXT, None),
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" and ", TextType.TEXT, None),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]

    def test_split_links_no_text_or_space_between(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
			TextNode("This is text with a link ", TextType.TEXT, None),
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
			TextNode(" and more", TextType.TEXT, None)
        ]

    def test_split_links_no_text_except_space(self):
        nodes = [
            TextNode("[to boot dev](https://www.boot.dev) [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" ", TextType.TEXT, None),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]

    def test_split_links_no_text_no_space(self):
        nodes = [
            TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]

    def test_split_links_wrong_text_type(self):
        try:
            nodes = [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.TEXT)
            ]
            new_nodes = split_nodes_links(nodes, TextType.ITALIC)
        except ValueError:
            assert True
        except Exception as e:
            assert False, f"split_nodes_links() raise {type(e).__name__} instead of ValueError"

    def test_split_links_text_type_link(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.LINK)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.LINK, None)
        ]

    def test_split_links_default_text_type(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes)
        assert new_nodes == [
			TextNode("This is text with a link ", TextType.TEXT, None),
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" and ", TextType.TEXT, None),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
			TextNode(" and more", TextType.TEXT, None)
        ]

    def test_split_links_no_links(self):
        nodes = [
            TextNode("This is text with a link to boot dev https://www.boot.dev and to youtube https://www.youtube.com/@bootdotdev and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
            TextNode("This is text with a link to boot dev https://www.boot.dev and to youtube https://www.youtube.com/@bootdotdev and more", TextType.TEXT, None)
        ]

    def test_split_links_bad_link_syntax(self):
        nodes =[
            TextNode("This is text with a link [to boot devhttps://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev and more", TextType.TEXT)
        ]
        new_nodes = split_nodes_links(nodes, TextType.LINK)
        assert new_nodes == [
            TextNode("This is text with a link [to boot devhttps://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev and more", TextType.TEXT, None)
        ]

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        assert extract_markdown_images(text) == [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    def test_extract_markdown_images_none_present(self):
        text = "This is text with a rick roll and obi wan"
        assert extract_markdown_images(text) == []

    def test_extract_markdown_images_bad_syntax(self):
        #bad syntax shouldn't cause errors, the pattern just won't match
        text = "This is text with a !rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wanhttps://i.imgur.com/fJRm4Vk.jpeg)"
        assert extract_markdown_images(text) == []

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        assert extract_markdown_links(text) == [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    def test_extract_markdown_links_none_present(self):
        text = "This is text with a link to boot dev and to youtube"
        assert extract_markdown_links(text) == []

    def test_extract_markdown_lists_bad_syntax(self):
        #bad syntax shouldn't cause errors, the pattern just won't match
        text = text = "This is text with a link to boot dev](https://www.boot.dev and [to youtubehttps://www.youtube.com/@bootdotdev)"
        assert extract_markdown_links(text) == []






    def test_split_nested_formatting(self):
        nodes = [TextNode("**bold and _italic_**", TextType.TEXT)]
        # Should only split outermost bold, not inner italic
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert result == [
            TextNode("bold and _italic_", TextType.BOLD)
        ]

    def test_split_escaped_delimiters(self):
        nodes = [TextNode(r"\*\*not bold\*\*", TextType.TEXT)]
        # Escaped delimiters should not be treated as formatting
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert result == [
            TextNode(r"\*\*not bold\*\*", TextType.TEXT)
        ]

    def test_split_delimiter_at_boundaries(self):
        nodes = [TextNode("**bold**text**more**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert result == [
            TextNode("bold", TextType.BOLD),
            TextNode("text", TextType.TEXT),
            TextNode("more", TextType.BOLD)
        ]

    def test_split_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert result == [
            TextNode("", TextType.TEXT)
        ]

    def test_split_whitespace_only(self):
        nodes = [TextNode("   ", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert result == [
            TextNode("   ", TextType.TEXT)
        ]

    def test_split_multiple_delimiters_sequence(self):
        nodes = [TextNode("**bold**_italic_", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        # Only bold is split, italic remains in text
        assert result == [
            TextNode("bold", TextType.BOLD),
            TextNode("_italic_", TextType.TEXT)
        ]

    def test_split_malformed_overlapping_markdown(self):
        # Overlapping delimiters, should treat as plain text
        nodes = [TextNode("**bold _italic** text_", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert result == [
            TextNode("bold _italic", TextType.BOLD),
            TextNode(" text_", TextType.TEXT)
        ]

    def test_extract_markdown_images_empty_alt(self):
        images = extract_markdown_images("![](url)")
        assert images == [("", "url")]

    def test_extract_markdown_links_empty_text(self):
        links = extract_markdown_links("[](url)")
        assert links == [("", "url")]

    def test_extract_markdown_links_empty_url(self):
        links = extract_markdown_links("[text]()")
        assert links == [("text", "")]




if __name__ == "__main__":
    unittest.main()
