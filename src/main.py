from textnode import TextNode, TextType


def main():
    textnode = TextNode(
        "This is some anchor text", TextType.ANCHOR, "https://www.boot.dev"
    )

    print(textnode)


if __name__ == "__main__":
    main()
