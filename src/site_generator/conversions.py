#!/usr/bin/python3

from .htmlnode import LeafNode
from .textnode import TextNode
from .enumerations import (
    TextType,
    BlockType
)
from .splits import (

    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links
)

def text_to_textnodes(text):
    original_node = TextNode(text, TextType.TEXT, None)
    bold_split = split_nodes_delimiter([original_node], "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_images(code_split)
    link_split = split_nodes_links(image_split)
    return link_split

def text_node_to_html_node(text_node):
    if text_node.text == None:
        raise ValueError("Text value cannot be None")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text type")

def markdown_to_blocks(markdown):
    md_lines = markdown.split("\n\n")
    blocks = []
    for block in md_lines:
        stripped_block = block.strip()
        if stripped_block != "":
            blocks.append(stripped_block)
    return blocks

def block_to_block_type(block):
    if block == None:
        raise ValueError("block value cannot be None")

    heading_values = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    if block.startswith(heading_values):
        return BlockType.HEAD

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        block_lines = block.split("\n")
        for line in block_lines:
            if not line.startswith(">"):
                return BlockType.PG
        return BlockType.QUOTE

    if block.startswith("- "):
        block_lines = block.split("\n")
        for line in block_lines:
            if not line.startswith("- "):
                return BlockType.PG
        return BlockType.UL

    if block.startswith("1. "):
        block_lines = block.split("\n")
        num_check = 0
        for line in block_lines:
            line_num = line[0]
            if line_num - num_check != 1:
                return BlockType.PG
            num_check += 1
        return BlockType.OL

    return BlockType.PG
