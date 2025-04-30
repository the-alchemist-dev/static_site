#!/usr/bin/python3

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from splitnodes import split_nodes_delimiter


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

    print("Basic test for splitting list of TextNodes that contain one other specified node type")
    example_nodes = [
        TextNode("Some of this text has _italic_ styling", TextType.TEXT, None),
        TextNode("This is more text with _italics_ in it", TextType.TEXT, None)
    ]
    split_nodes = split_nodes_delimiter(example_nodes, "_", TextType.ITALIC)
    for node in split_nodes:
        print(node)

main()
