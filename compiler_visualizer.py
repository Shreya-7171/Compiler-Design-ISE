import tkinter as tk


class CompilerVisualizer:

    BG = "#0f172a"
    PANEL = "#1e293b"
    PANEL2 = "#334155"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    GREEN = "#22c55e"
    BLUE = "#38bdf8"
    YELLOW = "#facc15"
    PURPLE = "#a78bfa"
    RED = "#fb7185"

    def __init__(
        self,
        tokens,
        tree,
        tac,
        optimized_tac,
        ai_report,
        target_code
    ):

        self.tokens = tokens
        self.tree = tree
        self.tac = tac
        self.optimized_tac = optimized_tac
        self.ai_report = ai_report
        self.target_code = target_code

        self.root = tk.Tk()
        self.root.title("RCL Compiler Visualizer")
        self.root.geometry("1250x780")
        self.root.configure(bg=self.BG)

        self.phase = 0

        self.phases = [
            "LEXICAL",
            "SYNTAX",
            "SEMANTIC",
            "TAC",
            "OPTIMIZATION + AI",
            "TARGET CODE"
        ]

        self.create_header()
        self.create_phase_bar()
        self.create_content()
        self.create_footer()

        self.root.after(500, self.show_phase)

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.BG
        )
        header.pack(fill="x", padx=30, pady=(20, 5))

        tk.Label(
            header,
            text="RCL COMPILER",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 26, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="Compiler Phase Visualizer",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 12)
        ).pack(side="right", pady=8)

    # =====================================================
    # PHASE BAR
    # =====================================================

    def create_phase_bar(self):

        self.phase_frame = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.phase_frame.pack(
            fill="x",
            padx=30,
            pady=15
        )

        self.phase_widgets = []

        for i, phase in enumerate(self.phases):

            frame = tk.Frame(
                self.phase_frame,
                bg=self.PANEL,
                height=55
            )

            frame.pack(
                side="left",
                fill="x",
                expand=True,
                padx=3
            )

            number = tk.Label(
                frame,
                text=str(i + 1),
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 11, "bold")
            )

            number.pack(
                side="left",
                padx=(10, 5)
            )

            label = tk.Label(
                frame,
                text=phase,
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 9, "bold")
            )

            label.pack(
                side="left"
            )

            self.phase_widgets.append(
                (frame, number, label)
            )

    # =====================================================
    # CONTENT
    # =====================================================

    def create_content(self):

        container = tk.Frame(
            self.root,
            bg=self.BG
        )

        container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        self.phase_title = tk.Label(
            container,
            text="",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 19, "bold")
        )

        self.phase_title.pack(
            anchor="w",
            pady=(5, 8)
        )

        self.status = tk.Label(
            container,
            text="",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 11)
        )

        self.status.pack(
            anchor="w",
            pady=(0, 12)
        )

        self.canvas = tk.Canvas(
            container,
            bg=self.PANEL,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # FOOTER
    # =====================================================

    def create_footer(self):

        self.footer = tk.Label(
            self.root,
            text="RCL Compiler • Lexical → Syntax → Semantic → TAC → Optimization → Target",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.footer.pack(
            pady=(5, 15)
        )

    # =====================================================
    # PHASE CONTROLLER
    # =====================================================

    def show_phase(self):

        self.canvas.delete("all")

        if self.phase >= len(self.phases):

            self.show_complete()
            return

        self.update_phase_bar()

        if self.phase == 0:
            self.show_lexer()

        elif self.phase == 1:
            self.show_parser()

        elif self.phase == 2:
            self.show_semantic()

        elif self.phase == 3:
            self.show_tac()

        elif self.phase == 4:
            self.show_optimizer()

        elif self.phase == 5:
            self.show_target()

    # =====================================================
    # UPDATE PHASE BAR
    # =====================================================

    def update_phase_bar(self):

        for i, widgets in enumerate(self.phase_widgets):

            frame, number, label = widgets

            if i < self.phase:

                frame.config(
                    bg="#14532d"
                )

                number.config(
                    bg="#14532d",
                    fg=self.GREEN
                )

                label.config(
                    bg="#14532d",
                    fg=self.TEXT
                )

            elif i == self.phase:

                frame.config(
                    bg="#075985"
                )

                number.config(
                    bg="#075985",
                    fg=self.BLUE
                )

                label.config(
                    bg="#075985",
                    fg=self.TEXT
                )

            else:

                frame.config(
                    bg=self.PANEL
                )

                number.config(
                    bg=self.PANEL,
                    fg=self.MUTED
                )

                label.config(
                    bg=self.PANEL,
                    fg=self.MUTED
                )

    # =====================================================
    # PHASE 1 - LEXER
    # =====================================================

    def show_lexer(self):

        self.phase_title.config(
            text="01  •  Lexical Analysis"
        )

        self.status.config(
            text="Scanning source code and generating tokens..."
        )

        items = []

        for token in self.tokens:

            token_type = getattr(
                token.type,
                "value",
                token.type
            )

            if token_type not in (
                "NEWLINE",
                "EOF"
            ):

                items.append(
                    f"{token_type:<12}  {str(token.value)}"
                )

        self.show_code_list(
            items,
            "TOKEN STREAM",
            self.BLUE,
            1
        )

    # =====================================================
    # PHASE 2 - PARSER
    # =====================================================

    def show_parser(self):

        self.phase_title.config(
            text="02  •  Syntax Analysis"
        )

        self.status.config(
            text="Building the syntax tree from the actual parser output..."
        )

        self.draw_tree(
            self.tree,
            600,
            60,
            None
        )

        self.root.after(
            3000,
            self.next_phase
        )

    # =====================================================
    # PARSE TREE
    # =====================================================

    def draw_tree(
        self,
        node,
        x,
        y,
        parent
    ):

        if parent is not None:

            parent_x, parent_y = parent

            self.canvas.create_line(
                parent_x,
                parent_y + 20,
                x,
                y - 20,
                fill=self.MUTED,
                width=2
            )

        name = str(node["name"])

        width = max(
            85,
            min(160, len(name) * 9 + 35)
        )

        self.canvas.create_rectangle(
            x - width / 2,
            y - 20,
            x + width / 2,
            y + 20,
            fill="#172554",
            outline=self.BLUE,
            width=2
        )

        self.canvas.create_text(
            x,
            y,
            text=name,
            fill=self.TEXT,
            font=("Segoe UI", 9, "bold")
        )

        children = node.get(
            "children",
            []
        )

        if not children:
            return

        spacing = min(
            200,
            1050 / len(children)
        )

        start_x = x - (
            spacing * (len(children) - 1) / 2
        )

        for i, child in enumerate(children):

            child_x = start_x + i * spacing
            child_y = y + 90

            self.draw_tree(
                child,
                child_x,
                child_y,
                (x, y)
            )

    # =====================================================
    # PHASE 3 - SEMANTIC
    # =====================================================

    def show_semantic(self):

        self.phase_title.config(
            text="03  •  Semantic Analysis"
        )

        self.status.config(
            text="Validating commands and maintaining robot state..."
        )

        commands = []

        for token in self.tokens:

            token_type = getattr(
                token.type,
                "value",
                token.type
            )

            if token_type in (
                "MOVE",
                "TURN",
                "PICK",
                "DROP",
                "WAIT"
            ):

                commands.append(
                    token_type
                )

        self.show_code_list(
            commands,
            "VALIDATED COMMANDS",
            self.GREEN,
            3
        )

    # =====================================================
    # PHASE 4 - TAC
    # =====================================================

    def show_tac(self):

        self.phase_title.config(
            text="04  •  Three Address Code"
        )

        self.status.config(
            text="Intermediate representation generated from the source program."
        )

        items = [
            str(instruction)
            for instruction in self.tac
        ]

        self.show_code_list(
            items,
            "GENERATED TAC",
            self.PURPLE,
            4
        )

    # =====================================================
    # PHASE 5 - OPTIMIZATION + AI
    # =====================================================

    def show_optimizer(self):

        self.phase_title.config(
            text="05  •  Optimization + AI"
        )

        self.status.config(
            text="Optimizing intermediate code and generating AI analysis..."
        )

        # LEFT PANEL

        self.canvas.create_text(
            280,
            35,
            text="OPTIMIZED TAC",
            fill=self.TEXT,
            font=("Segoe UI", 14, "bold")
        )

        y = 75

        for instruction in self.optimized_tac:

            self.canvas.create_rectangle(
                50,
                y - 16,
                510,
                y + 16,
                fill="#312e81",
                outline=self.PURPLE
            )

            self.canvas.create_text(
                280,
                y,
                text=str(instruction),
                fill=self.TEXT,
                font=("Consolas", 10)
            )

            y += 42

        # DIVIDER

        self.canvas.create_line(
            600,
            25,
            600,
            500,
            fill=self.PANEL2,
            width=2
        )

        # RIGHT PANEL

        self.canvas.create_text(
            875,
            35,
            text="AI OPTIMIZATION REPORT",
            fill=self.TEXT,
            font=("Segoe UI", 14, "bold")
        )

        report = str(
            self.ai_report
        )

        self.canvas.create_text(
            630,
            75,
            text=report[:1800],
            fill=self.MUTED,
            font=("Segoe UI", 10),
            width=500,
            anchor="nw"
        )

        self.root.after(
            4000,
            self.next_phase
        )

    # =====================================================
    # PHASE 6 - TARGET CODE
    # =====================================================

    def show_target(self):

        self.phase_title.config(
            text="06  •  Target Code Generation"
        )

        self.status.config(
            text="Converting optimized TAC into final target instructions..."
        )

        items = [
            str(line)
            for line in self.target_code
        ]

        self.show_code_list(
            items,
            "FINAL TARGET CODE",
            self.YELLOW,
            6
        )

    # =====================================================
    # CODE / LIST DISPLAY
    # =====================================================

    def show_code_list(
        self,
        items,
        title,
        accent,
        next_phase
    ):

        self.canvas.create_text(
            575,
            35,
            text=title,
            fill=self.TEXT,
            font=("Segoe UI", 14, "bold")
        )

        self.animate_items(
            items,
            0,
            80,
            accent,
            next_phase
        )

    def animate_items(
        self,
        items,
        index,
        y,
        accent,
        next_phase
    ):

        if index >= len(items):

            self.root.after(
                1200,
                lambda: self.go_to_phase(next_phase)
            )

            return

        self.canvas.create_rectangle(
            280,
            y - 17,
            870,
            y + 17,
            fill=self.PANEL2,
            outline=accent,
            width=1
        )

        self.canvas.create_text(
            575,
            y,
            text=str(items[index]),
            fill=self.TEXT,
            font=("Consolas", 11)
        )

        self.root.after(
            350,
            lambda: self.animate_items(
                items,
                index + 1,
                y + 38,
                accent,
                next_phase
            )
        )

    # =====================================================
    # NEXT PHASE
    # =====================================================

    def next_phase(self):

        self.phase += 1
        self.show_phase()

    def go_to_phase(self, phase):

        self.phase = phase
        self.show_phase()

    # =====================================================
    # COMPLETE
    # =====================================================

    def show_complete(self):

        for frame, number, label in self.phase_widgets:

            frame.config(
                bg="#14532d"
            )

            number.config(
                bg="#14532d",
                fg=self.GREEN
            )

            label.config(
                bg="#14532d",
                fg=self.TEXT
            )

        self.phase_title.config(
            text="✓  Compilation Successful"
        )

        self.status.config(
            text="All six compiler phases completed successfully."
        )

        self.canvas.delete("all")

        self.canvas.create_text(
            575,
            210,
            text="✓",
            fill=self.GREEN,
            font=("Segoe UI", 65, "bold")
        )

        self.canvas.create_text(
            575,
            300,
            text="RCL PROGRAM COMPILED SUCCESSFULLY",
            fill=self.TEXT,
            font=("Segoe UI", 22, "bold")
        )

        self.canvas.create_text(
            575,
            345,
            text="Source → Tokens → Syntax Tree → Semantic Checks → TAC → AI Optimization → Target Code",
            fill=self.MUTED,
            font=("Segoe UI", 11)
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        self.root.mainloop()