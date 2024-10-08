import os
import shutil


def main():
    # text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    # print(text_node)
    copy_dir("static", "public")


def copy_dir(source, destination):

    if os.path.exists(destination):
        for item in os.listdir(destination):
            path = os.path.join(destination, item)
            if os.path.isfile(path):
                print(f"Deleting {path}")
                os.remove(path)
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


if __name__ == "__main__":
    main()
