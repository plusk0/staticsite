from textnode import *

def main():
    TestNode = TextNode("Some anchor text", TextType.LINK, "https://boot.dev")
    print(str(TestNode.__repr__()))

main()
