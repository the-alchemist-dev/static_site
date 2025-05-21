#!/usr/bin/python3

from site_generator.conversions import *
from site_generator.enumerations import *
from site_generator.htmlnode import *
from site_generator.splits import *
from site_generator.textnode import *


def main():
    print("\n\nBasic test for TextNode\n")
    example_text = TextNode("This is anchor text", TextType.LINK, "https://www.boot.dev")
    print(example_text, "\n\n")

    print("Basic test for converting TextNode to (new) LeafNode\n")
    html_from_text = text_node_to_html_node(example_text)
    print(html_from_text)
    print(html_from_text.to_html(), "\n\n")

    print("Basic test for HTMLNode\n")
    example_html = HTMLNode("h1", "This Is A Header", None, {"href": "https://www.google.com", "target": "_blank"})
    print(example_html, "\n\n")

    print("Basic test for LeafNode\n")
    example_leaf = LeafNode("a", "This is a link", {"href": "https://www.boot.dev"})
    print(example_leaf)
    print(example_leaf.to_html(), "\n\n")

    print("Basic test for ParentNode\n")
    example_parent = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(example_parent)
    print(example_parent.to_html(), "\n\n")

    print("Basic test for splitting list of TextNodes that contain one other specified node type\n")
    example_nodes = [
        TextNode("Some of this text has _italic_ styling", TextType.TEXT, None),
        TextNode("This is more text with _italics_ in it", TextType.TEXT, None)
    ]
    split_nodes = split_nodes_delimiter(example_nodes, "_", TextType.ITALIC)
    for node in split_nodes:
        print(node)
    print("\n\n")

    print("Basic test for extracting images and links from markdown\n")
    image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_images(image_text))
    print(extract_markdown_links(link_text), "\n\n")

    print("Basic test for splitting nodes containing images\n")
    image_node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and more", TextType.TEXT)
    split_nodes = split_nodes_images([image_node], TextType.IMAGE)
    for node in split_nodes:
        print(node)
    print("\n\n")

    print("Basic test for splitting nodes containing links\n")
    link_node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more", TextType.TEXT)
    split_nodes = split_nodes_links([link_node], TextType.LINK)
    for node in split_nodes:
        print(node)
    print("\n\n")

    print("Basic test for splitting all elements out of text into new nodes\n")
    example_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(example_text)
    print(nodes)

main()
