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
