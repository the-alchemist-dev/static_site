#!/usr/bin/python3

from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import LeafNode

def main():
    example_text = TextNode("This is anchor text", "link", "https://www.boot.dev")
    print(example_text)

    example_html = HTMLNode("h1", "This Is A Header", None, {"href": "https://www.google.com", "target": "_blank"})
    print(example_html)

    example_leaf = LeafNode("a", "This is a link", {"href": "https://www.boot.dev"})
    print(example_leaf)
    print(example_leaf.to_html())

main()
