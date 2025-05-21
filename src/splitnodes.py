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
            i = 0
            while i < len(split_text):
                text_item = split_text[i]
                if text_item != "":
                    # Even index: plain text
                    new_nodes.append(TextNode(text_item, TextType.TEXT))
                i += 1
                # If there's a next item, it's a candidate for markdown
                if i < len(split_text):
                    # If this is the last item and there's no closing delimiter, treat as plain text with delimiter
                    if i == len(split_text) - 1:
                        unmatched = delimiter + split_text[i]
                        if split_text[i] != "":
                            new_nodes.append(TextNode(unmatched, TextType.TEXT))
                    else:
                        if split_text[i] != "":
                            new_nodes.append(TextNode(split_text[i], text_type))
                    i += 1
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_images(old_nodes, text_type=TextType.IMAGE):
    valid_text_types = [TextType.IMAGE]
    if text_type not in valid_text_types:
        raise ValueError(f"Invalid text_type value, must be {valid_text_types}")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.IMAGE:
            images = extract_markdown_images(node.text)
            if images != []:
                working_text = node.text
                for image in images:
                    image_alt = image[0]
                    image_src = image[1]
                    sections = working_text.split(f"![{image_alt}]({image_src})", 1)
                    left_split = sections[0]
                    right_split = sections[1]
                    if left_split != "" and right_split != "":
                        new_nodes.append(TextNode(left_split, TextType.TEXT))
                        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_src))
                        image_check = extract_markdown_images(right_split)
                        if image_check == []:
                            new_nodes.append(TextNode(right_split, TextType.TEXT))
                        else:
                            working_text = right_split
                    elif left_split != "" and right_split == "":
                        new_nodes.append(TextNode(left_split, TextType.TEXT))
                        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_src))
                    elif left_split == "" and right_split != "":
                        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_src))
                        image_check = extract_markdown_images(right_split)
                        if image_check == []:
                            new_nodes.append(TextNode(right_split, TextType.TEXT))
                        else:
                            working_text = right_split
                    else:
                        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_src))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_links(old_nodes, text_type=TextType.LINK):
    valid_text_types = [TextType.LINK]
    if text_type not in valid_text_types:
        raise ValueError(f"Invalid text_type value, must be {valid_text_types}")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.LINK:
            links = extract_markdown_links(node.text)
            if links != []:
                working_text = node.text
                for link in links:
                    link_text = link[0]
                    link_url = link[1]
                    sections = working_text.split(f"[{link_text}]({link_url})", 1)
                    left_split = sections[0]
                    right_split = sections[1]
                    if left_split != "" and right_split != "":
                        new_nodes.append(TextNode(left_split, TextType.TEXT))
                        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                        link_check = extract_markdown_links(right_split)
                        if link_check == []:
                            new_nodes.append(TextNode(right_split, TextType.TEXT))
                        else:
                            working_text = right_split
                    elif left_split != "" and right_split == "":
                        new_nodes.append(TextNode(left_split, TextType.TEXT))
                        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                    elif left_split == "" and right_split != "":
                        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                        link_check = extract_markdown_links(right_split)
                        if link_check == []:
                            new_nodes.append(TextNode(right_split, TextType.TEXT))
                        else:
                            working_text = right_split
                    else:
                        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links
