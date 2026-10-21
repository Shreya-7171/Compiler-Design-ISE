class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, value=None):

        # Add or update symbol
        self.symbols[name] = value
        return True

    def exists(self, name):

        return name in self.symbols

    def get_symbol(self, name):

        return self.symbols.get(name)

    def display(self):

        for name, value in self.symbols.items():
            print(name, ":", value)