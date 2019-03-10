import collections
from AST import NodeVisitor

class Symbol():

    def __init__(self, name, Type=None):
        self.name = name
        self.type = Type


class BuiltinTypeSymbol(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class VarSymbol(Symbol):

    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f"<{self.name}:{self.type}>"

    __repr__ = __str__


class SymbolTable():

    def __init__(self):

        self.symbols = collections.OrderedDict()

    def __str__(self):

        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self.symbols.values()]
        )

        return s

    def define(self, symbol):
        print(f'Define: {symbol.name}')
        self.symbols[symbol.name] = symbol

    def lockup(self, name):
        print('Lookup: %s' % name)
        symbol = self.symbols.get(name)
        return symbol


