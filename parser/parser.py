from parser.parser_part_a import ParserPartA
from parser.parser_part_b import ParserPartB


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.tree = {
            "name": "Program",
            "children": []
        }

    def parse(self):

        while self.current < len(self.tokens):

            token = self.tokens[self.current]

            if token.type == "NEWLINE":
                self.current += 1
                continue

            if token.type == "EOF":
                break

            if token.type == "START":

                parser = ParserPartA(self.tokens[self.current:])
                parser.parse_start()

                self.tree["children"].append({
                    "name": "START",
                    "children": []
                })

            elif token.type == "END":

                parser = ParserPartA(self.tokens[self.current:])
                parser.parse_end()

                self.tree["children"].append({
                    "name": "END",
                    "children": []
                })

            elif token.type == "MOVE":

                parser = ParserPartA(self.tokens[self.current:])
                parser.parse_move()

                direction = self.tokens[self.current + 1]
                number = self.tokens[self.current + 2]

                self.tree["children"].append({
                    "name": "MOVE",
                    "children": [
                        {
                            "name": direction.value,
                            "children": []
                        },
                        {
                            "name": f"NUMBER: {number.value}",
                            "children": []
                        }
                    ]
                })

            elif token.type == "TURN":

                parser = ParserPartA(self.tokens[self.current:])
                parser.parse_turn()

                direction = self.tokens[self.current + 1]

                self.tree["children"].append({
                    "name": "TURN",
                    "children": [
                        {
                            "name": direction.value,
                            "children": []
                        }
                    ]
                })

            elif token.type == "PICK":

                parser = ParserPartB(self.tokens[self.current:])
                parser.parse_pick()

                self.tree["children"].append({
                    "name": "PICK",
                    "children": []
                })

            elif token.type == "DROP":

                parser = ParserPartB(self.tokens[self.current:])
                parser.parse_drop()

                self.tree["children"].append({
                    "name": "DROP",
                    "children": []
                })

            elif token.type == "WAIT":

                parser = ParserPartB(self.tokens[self.current:])
                parser.parse_wait()

                number = self.tokens[self.current + 1]

                self.tree["children"].append({
                    "name": "WAIT",
                    "children": [
                        {
                            "name": f"NUMBER: {number.value}",
                            "children": []
                        }
                    ]
                })

            else:

                raise SyntaxError(
                    f"Unexpected token at line {token.line}, "
                    f"column {token.column}: {token.value}"
                )

            self.current += parser.current

        return self.tree


def print_tree(node, prefix="", is_last=True):

    if prefix == "":
        print(node["name"])
    else:
        connector = "└── " if is_last else "├── "
        print(prefix + connector + node["name"])

    children = node["children"]

    for i, child in enumerate(children):

        last = i == len(children) - 1

        if prefix == "":
            child_prefix = ""
        else:
            child_prefix = prefix + (
                "    " if is_last else "│   "
            )

        print_tree(child, child_prefix, last)