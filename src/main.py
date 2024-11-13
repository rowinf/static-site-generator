import os
import shutil
import stat
import io

from markdown_processing import extract_title, markdown_to_html_node


def copy_files(srcdir, destdir):
    for name in os.listdir(srcdir):
        print(name)
        pathname = os.path.join(srcdir, name)
        destpath = os.path.join(destdir, name)
        mode = os.lstat(pathname).st_mode
        if stat.S_ISDIR(mode):
            os.mkdir(destpath)
            copy_files(pathname, destpath)
        elif stat.S_ISREG(mode):
            shutil.copy(pathname, destpath)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    tfile = io.open(template_path)
    template = tfile.read()
    for f in os.listdir(from_path):
        cfile = io.open(os.path.join(from_path, f))
        markdown = cfile.read()
        title = extract_title(markdown)
        with io.open(os.path.join(dest_path, "index.html"), "w") as outfile:
            nodes = markdown_to_html_node(markdown)
            updated = template.replace("{{ Title }}", title).replace(
                "{{ Content }}", nodes.to_html()
            )
            outfile.write(updated)
        cfile.close()
    tfile.close()


def main():
    try:
        shutil.rmtree("./public")
    finally:
        os.mkdir("./public")
    print("\n\ncopying files...")
    copy_files("./static", "./public")
    generate_page("./content", "./template.html", "./public/")


if __name__ == "__main__":
    main()
