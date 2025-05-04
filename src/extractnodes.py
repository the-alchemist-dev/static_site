#!/usr/bin/python3

import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_delimiters = ["**", "`", "_"]
    valid_text_types = [TextType.BOLD, TextType.ITALIC, TextType.CODE]
    if delimiter not in valid_delimiters:
        raise ValueError(f"Invalid delimiter value, must be one of {valid_delimiters}")
    if text_type not in valid_text_types:
        raise ValueError(f"Invalid text_type value, must be one of {valid_text_types}")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter in node.text:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("Invalid markdown syntax: must have opening and closing flags")
            for index, text_item in enumerate(split_text):
                if text_item != "":
                    if index % 2 == 0:
                        new_nodes.append(TextNode(text_item, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text_item, text_type))
    return new_nodes

def split_nodes_images(old_nodes, text_type):
    valid_text_types = [TextType.IMAGE]
    if text_type not in valid_text_types:
        raise ValueError(f"Invalid text_type value, must be {valid_text_types}")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.IMAGE:
            images = extract_markdown_images(node)
            if images != []:
                for image in images:
                    sections = node.text.split(f"![{image_alt}]({image_link})", 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_links(old_nodes, text_type):
    valid_text_types = [TextType.LINK]

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images
    
def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links
