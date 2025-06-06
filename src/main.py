from textnode import TextNode
from fixed_variables import TextType

def main():
    TestNode = TextNode("Some anchor text", TextType.LINK, "https://boot.dev")
    print(TestNode)

main()
