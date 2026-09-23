class SymbolTable:

    def __init__(self):
        self.symbols = {}

    # Add a symbol to the table
    def add_symbol(self, name, value=None):
        if name in self.symbols:
            return False

        self.symbols[name] = value
        return True

    # Check whether a symbol exists
    def exists(self, name):
        return name in self.symbols

    # Get the value of a symbol
    def get_symbol(self, name):
        return self.symbols.get(name)

    # Display all symbols
    def display(self):
        for name, value in self.symbols.items():
            print(name, ":", value)


# Simple test
if __name__ == "__main__":

    table = SymbolTable()

    print(table.add_symbol("distance", 10))
    print(table.add_symbol("direction", "LEFT"))

    print(table.exists("distance"))
    print(table.exists("speed"))

    table.display()