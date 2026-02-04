import os
from helper_funcs import markdown_to_html_node
from pathlib import Path


class GeneratePage:
    def __init__(self, from_path, template_path, dest_path):
        self.from_path = from_path
        self.template_path = template_path
        self.dest_path = dest_path
        self.html = None

    def generate_pages_recursive(self, from_path=None, dest_path=None):
        from_path = from_path or self.from_path
        dest_path = dest_path or self.dest_path

        print(
            f"Generating pages from {from_path} to {dest_path} using {self.template_path}"
        )

        for entry in os.listdir(from_path):
            entry_path = os.path.join(from_path, entry)
            dest_entry_path = os.path.join(dest_path, entry)

            if os.path.isfile(entry_path):
                dest_path_html = Path(dest_entry_path).with_suffix(".html")
                self.generate_page(entry_path, dest_path_html)
            else:
                os.makedirs(dest_entry_path, exist_ok=True)
                self.generate_pages_recursive(entry_path, dest_entry_path)

    def generate_page(self, from_path, dest_path):
        print(
            f"Generating page from {from_path} to {dest_path} using {self.template_path}"
        )

        with open(from_path, "r", encoding="utf-8") as f:
            markdown = f.read()

        with open(self.template_path, "r", encoding="utf-8") as f:
            template = f.read()

        content = markdown_to_html_node(markdown).to_html()
        title = self.extract_title(markdown)
        template = template.replace("{{ Title }}", title).replace(
            "{{ Content }}", content
        )

        path = Path(dest_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template)

    def extract_title(self, markdown):
        for line in markdown.splitlines():
            if line.startswith("# "):
                return line[2:].strip()

        raise ValueError("no title header found")
