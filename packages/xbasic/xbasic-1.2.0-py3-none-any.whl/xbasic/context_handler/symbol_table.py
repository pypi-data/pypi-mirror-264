class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.data_types = {}

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set_data_type(self, var_name, data_type):
        self.data_types[var_name] = data_type

    def get_data_type(self, var_name):
        return self.data_types.get(var_name)

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
