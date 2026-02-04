from pathlib import Path
from generate_static import generate_static
from generate_page import GeneratePage

BASE_DIR = Path(__file__).resolve().parent


def main():
    source = BASE_DIR.parent / "static"
    target = BASE_DIR.parent / "public"
    from_path = BASE_DIR.parent / "content"
    template = BASE_DIR.parent / "template.html"
    dest_path = target
    generate_static(source, target)

    page_gen = GeneratePage(from_path, template, dest_path)
    page_gen.generate_pages_recursive()


if __name__ == "__main__":
    main()
