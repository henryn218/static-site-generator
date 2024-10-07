import re


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
        return "ordered_list"
    else:
        return "paragraph"
