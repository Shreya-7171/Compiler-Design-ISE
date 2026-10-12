from semantic.symbol_table import SymbolTable


def test_variable_added_to_symbol_table():

    table = SymbolTable()

    table.add_symbol("distance", 10)

    assert table.exists("distance")


def test_variable_value():

    table = SymbolTable()

    table.add_symbol("distance", 10)

    assert table.get_symbol("distance") == 10