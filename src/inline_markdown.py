import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ("`", "*", "**"):
        raise ValueError(f"Cannot handle '{delimiter}' delimiter")

    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT or not is_valid_markdown(
            node.text, delimiter
        ):
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node_text_delimiter(node.text, delimiter, text_type))

    return new_nodes


def split_node_text_delimiter(
    text, delimiter, text_type, inside_delimiter_pair=False, text_nodes=None
):
    if text_nodes is None:
        text_nodes = []

    text_split = split_text(text, delimiter)

    if text_split and text_split[0] != "":
        text_nodes.append(
            TextNode(
                text_split[0], text_type if inside_delimiter_pair else TextType.TEXT
            )
        )

    if len(text_split) > 1 and text_split[1] != "":
        return split_node_text_delimiter(
            text_split[1], delimiter, text_type, not inside_delimiter_pair, text_nodes
        )
    else:
        return text_nodes


def split_text(text, delimiter):
    if delimiter == "*":
        if len(set(text)) == 1:
            return [""]
        substring_one = ""
        break_position = 0
        delimiter_count = 0
        for i, character in enumerate(text):
            if character == delimiter:
                delimiter_count += 1
                if (
                    i == len(text) - 1 or text[i + 1] != delimiter
                ) and delimiter_count < 2:
                    break_position = i + 1
                    break
                if delimiter_count > 1:
                    delimiter_count = 0
            substring_one += character
        else:
            break_position = len(text)
        substring_two = text[break_position:]
        return [substring_one, substring_two]
    else:
        return text.split(delimiter, maxsplit=1)


def is_valid_markdown(text, delimiter):
    return not bool(text.count(delimiter) % 2)


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes(old_nodes, markdown_extractor, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        items = markdown_extractor(node_text)

        if not items:
            new_nodes.append(node)
            continue

        for text, link in items:
            item_markdown = get_link_or_image_markdown_format(text, link, text_type)
            node_text_split = node_text.split(item_markdown, maxsplit=1)
            if node_text_split and node_text_split[0] != "":
                new_nodes.append(TextNode(node_text_split[0], TextType.TEXT))
            if len(node_text_split) > 1:
                node_text = node_text_split[1]
            new_nodes.append(TextNode(text, text_type, link))
        else:
            if node_text:
                new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, extract_markdown_links, TextType.LINK)


def get_link_or_image_markdown_format(text, link, text_type):
    match text_type:
        case TextType.LINK:
            return f"[{text}]({link})"
        case TextType.IMAGE:
            return f"![{text}]({link})"
        case _:
            raise ValueError("text_type must be one of LINK or IMAGE")


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for text_type, delimiter in [
        (TextType.CODE, "`"),
        (TextType.BOLD, "**"),
        (TextType.ITALIC, "*"),
    ]:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
