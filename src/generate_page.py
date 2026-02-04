from helper_funcs import markdown_to_html_node
from pathlib import Path


class GeneratePage:
    def __init__(self, from_path, template_path, dest_path):
        self.from_path = from_path
        self.template_path = template_path
        self.dest_path = dest_path
        self.markdown = None
        self.template = None
        self.html = None

    def generate_page(self):
        print(
            f"Generating page from {self.from_path} to {self.dest_path} using {self.template_path}"
        )

        with open(self.from_path, "r", encoding="utf=8") as f:
            self.markdown = f.read()

        with open(self.template_path, "r", encoding="utf-8") as f:
            self.template = f.read()

        content = markdown_to_html_node(self.markdown).to_html()
        title = self.extract_title()
        self.template = self.template.replace("{{ Title }}", title).replace(
            "{{ Content }}", content
        )

        path = Path(self.dest_path)
        path.write_text(self.template)

    def extract_title(self):
        lines = self.markdown.split("\n")
        title = None
        for line in lines:
            if line.startswith("# "):
                parts = line.split("# ")
                title = parts[1]
        if not title:
            raise Exception("no title header found")

        return title
