import tkinter as tk


class TreeVisualizer:

    def __init__(self, tree):

        self.tree = tree
        self.nodes = []
        self.positions = {}
        self.current_node = 0

        self.root = tk.Tk()
        self.root.title("RCL Compiler - Syntax Analysis")
        self.root.geometry("1200x750")

        title = tk.Label(
            self.root,
            text="RCL COMPILER - SYNTAX ANALYSIS",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        self.status = tk.Label(
            self.root,
            text="Generating Parse Tree...",
            font=("Arial", 13)
        )
        self.status.pack(pady=5)

        self.canvas = tk.Canvas(
            self.root,
            width=1150,
            height=620,
            bg="white"
        )
        self.canvas.pack(padx=20, pady=10)

        self.prepare_nodes(
            self.tree,
            None,
            0
        )

        self.calculate_positions()

        self.root.after(
            500,
            self.animate
        )

    def prepare_nodes(self, node, parent, depth):

        node_id = len(self.nodes)

        self.nodes.append({
            "id": node_id,
            "name": node["name"],
            "parent": parent,
            "depth": depth
        })

        for child in node.get("children", []):

            self.prepare_nodes(
                child,
                node_id,
                depth + 1
            )

    def calculate_positions(self):

        levels = {}

        for node in self.nodes:

            depth = node["depth"]

            if depth not in levels:
                levels[depth] = []

            levels[depth].append(node)

        for depth, nodes in levels.items():

            count = len(nodes)

            if count == 1:

                x_positions = [575]

            else:

                spacing = 1050 / (count + 1)

                x_positions = []

                for i in range(count):

                    x = 75 + spacing * (i + 1)
                    x_positions.append(x)

            for i, node in enumerate(nodes):

                x = x_positions[i]
                y = 70 + depth * 100

                self.positions[node["id"]] = (
                    x,
                    y
                )

    def draw_node(self, node):

        node_id = node["id"]
        name = node["name"]

        x, y = self.positions[node_id]

        width = max(
            90,
            len(name) * 10 + 30
        )

        height = 45

        if node["parent"] is not None:

            parent_id = node["parent"]

            parent_x, parent_y = self.positions[parent_id]

            self.canvas.create_line(
                parent_x,
                parent_y + 22,
                x,
                y - 22,
                width=2
            )

        self.canvas.create_rectangle(
            x - width / 2,
            y - height / 2,
            x + width / 2,
            y + height / 2,
            outline="black",
            width=2
        )

        self.canvas.create_text(
            x,
            y,
            text=name,
            font=("Arial", 11, "bold")
        )

    def animate(self):

        if self.current_node < len(self.nodes):

            node = self.nodes[self.current_node]

            self.draw_node(node)

            self.current_node += 1

            self.status.config(
                text=(
                    "Generating Parse Tree... "
                    + str(self.current_node)
                    + " / "
                    + str(len(self.nodes))
                    + " nodes"
                )
            )

            self.root.after(
                600,
                self.animate
            )

        else:

            self.status.config(
                text="Syntax Analysis Successful - Parse Tree Generated"
            )

    def run(self):

        self.root.mainloop()