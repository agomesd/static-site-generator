from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag in ParentNode")

        if not self.children:
            raise ValueError("missing children in ParentNode")
        children_html = ""

        for child_node in self.children:
            children_html += child_node.to_html()

        if self.props:
            props = self.props_to_html()
            return f"<{self.tag}{props}>{children_html}</{self.tag}>"

        return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
