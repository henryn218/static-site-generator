import re

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(tuple("#" * x + " " for x in range(1, 7))):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(x.startswith(">") for x in lines):
        return "quote"
    elif all(x.startswith("* ") for x in lines):
        return "unordered_list"
    elif all(x.startswith("- ") for x in lines):
        return "unordered_list"
    elif all(re.match(r"^\d\. ", x) for x in lines):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                break
        else:
            return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown):
    children_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            children_nodes.append(make_heading_html_node(block))
        elif block_type == "code":
            code_node = LeafNode(block.strip("```").strip(), "code")
            children_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == "quote":
            children_nodes.append(make_quote_html_node(block))
        elif block_type in ("unordered_list", "ordered_list"):
            children_nodes.append(make_list_html_node(block, block_type))
        elif block_type == "paragraph":
            children_nodes.append(make_paragraph_html_node(block))

    return ParentNode("div", children_nodes)


def make_heading_html_node(block):
    block_no_markdown = block.lstrip("#")
    heading_tag = f"h{len(block) - len(block_no_markdown)}"
    return LeafNode(block_no_markdown.strip(), heading_tag)


def make_paragraph_html_node(block):
    paragraph = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph))


def make_quote_html_node(block):
    return ParentNode(
        "blockquote",
        text_to_children(block.lstrip(">").replace("\n>", "").strip()),
    )


def make_list_html_node(block, list_type):
    if list_type == "unordered_list":
        list_marker_stripper = strip_unordered_list_marker
        list_tag = "ul"
    elif list_type == "ordered_list":
        list_marker_stripper = strip_ordered_list_marker
        list_tag = "ol"
    else:
        raise ValueError("List type must be one of 'unordered' or 'ordered'")

    lines = block.split("\n")
    stripped_lines = list_marker_stripper(lines)
    list_nodes = []
    for line in stripped_lines:
        list_item_children = text_to_children(line)
        list_nodes.append(ParentNode("li", list_item_children))
    return ParentNode(list_tag, list_nodes)


def strip_ordered_list_marker(lines):
    return (text.lstrip(f"{i + 1}. ") for i, text in enumerate(lines))


def strip_unordered_list_marker(lines):
    if lines[0].startswith("*"):
        list_marker = "* "
    elif lines[0].startswith("- "):
        list_marker = "- "
    else:
        raise ValueError("Unordered lists must use '-' or '*' to indicate list items")

    return (text.strip(list_marker) for text in lines)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]
