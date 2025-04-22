#!/usr/bin/python3

from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

def main():
    example_text = TextNode("This is anchor text", "link", "https://www.boot.dev")
    print(example_text)

    example_html = HTMLNode("h1", "This Is A Header", None, {"href": "https://www.google.com", "target": "_blank"})
    print(example_html)

    example_leaf = LeafNode("a", "This is a link", {"href": "https://www.boot.dev"})
    print(example_leaf)
    print(example_leaf.to_html())

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
    print(example_parent.to_html())    

main()
