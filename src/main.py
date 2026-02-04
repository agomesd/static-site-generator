from pathlib import Path
from generate_static import generate_static
from generate_page import generate_pages_recursive
import sys

BASE_DIR = Path(__file__).resolve().parent


def main():
    basepath = sys.argv[0] or "/"

    source = BASE_DIR.parent / "static"
    target = BASE_DIR.parent / "docs"
    from_path = BASE_DIR.parent / "content"
    template = BASE_DIR.parent / "template.html"
    dest_path = target
    generate_static(source, target)

    print("Generating content...")
    generate_pages_recursive(from_path, template, dest_path, basepath)


if __name__ == "__main__":
    main()
