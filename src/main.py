import os
import shutil
import stat

from textnode import TextNode, TextType


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


def main():
    try:
        shutil.rmtree("./public")
    finally:
        os.mkdir("./public")
    copy_files("./static", "./public")


if __name__ == "__main__":
    main()
