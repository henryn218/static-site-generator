import os
import shutil

from markdown_blocks import markdown_to_html_node


def delete_dir_contents(dir):
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            print(f"Deleting {path}")
            os.remove(path)


def copy_dir(source, destination):

    if os.path.exists(destination):
        delete_dir_contents(destination)
    else:
        os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        print(f"Copying {source_path} -> {destination_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            copy_dir(source_path, destination_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("#").strip()
    raise ValueError("No title line found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()
    title = extract_title(markdown)
    html_page = template.replace("{{ Content }}", content_html).replace(
        "{{ Title }}", title
    )
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(dest_path, "w") as f:
        f.write(html_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isfile(path):
            name, _ = os.path.splitext(item)
            dest_path = os.path.join(dest_dir_path, f"{name}.html")
            generate_page(path, template_path, dest_path)
        elif os.path.isdir(path):
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(path, template_path, dest_path)
