#!/usr/bin/python3

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        if delimiter in node.text:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Invalid markdown syntax: matching delimiters required")
            for index, text_item in enumerate(split_text):
                if text_item != "":
                    if index % 2 == 0:
                        new_nodes.append(TextNode(text_item, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text_item, text_type))
        return new_nodes
