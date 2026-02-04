import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)
        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            before, text = text.split(image_markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        for value, url in links:
            link_markdown = f"[{value}]({url})"

            before, text = text.split(link_markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(value, TextType.ANCHOR, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    clean_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block != "":
            clean_blocks.append(block.strip())

    return clean_blocks


def block_to_block_type(block):
    if re.match(r"^(#{1,6})\s+(.*)", block):
        return BlockType.HEADING
    elif re.match(r"^```(\w+)?\n.*?```$", block, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^>\s?(.*)", block):
        return BlockType.QUOTE
    elif re.match(r"^- (.*)", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^(\d+)\. (.*)", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes = block_to_html_node(block, block_type)
        children.append(html_nodes)

    div = ParentNode("div", children)
    return div


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(node.text_node_to_html_node())

    return html_nodes


def block_to_html_node(block, block_type):
    if block_type == BlockType.CODE:
        return code_block_to_children(block)
    match block_type:
        case BlockType.PARAGRAPH:
            cleaned = " ".join(block.splitlines())
            children = text_to_children(cleaned)

            if len(children) == 1 and getattr(children[0], "tag", None) == "img":
                return children[0]

            return ParentNode("p", children)
        case BlockType.HEADING:
            return block_to_heading_html_node(block)
        case BlockType.UNORDERED_LIST:
            children = unordered_list_block_to_children(block)
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = ordered_list_block_to_children(block)
            return ParentNode("ol", children)
        case BlockType.QUOTE:
            return quote_block_to_children(block)
        case _:
            raise Exception(f"invalid BlockType: {block_type}")


def block_to_heading_html_node(block):
    first_space = block.find(" ")
    hashes = block[:first_space]
    heading = block[first_space + 1 :]

    children = text_to_children(heading)
    return ParentNode(f"h{len(hashes)}", children)


def unordered_list_block_to_children(block):
    lines = block.splitlines()
    list_items = []
    for line in lines:
        text = line.split("- ")[1]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return list_items


def ordered_list_block_to_children(block):
    lines = block.splitlines()
    list_items = []
    for line in lines:
        text = line.split(".", 1)[1]
        children = text_to_children(text.strip())
        list_items.append(ParentNode("li", children))

    return list_items


def code_block_to_children(block):
    lines = block.splitlines()
    inner = "\n".join(lines[1:-1]) + "\n"
    text_node = TextNode(inner, TextType.CODE)
    code_node = text_node.text_node_to_html_node()
    return ParentNode("pre", [code_node])


def quote_block_to_children(block):
    lines = block.splitlines()
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    print(content)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
