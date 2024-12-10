class TomlGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.output = []

    def generate(self):
        for node in self.ast:
            if node is None:
                continue
            if node[0] == 'SET':
                self.generate_set(node)
            elif node[0] == 'ARRAY':
                self.generate_array(node)
            elif node[0] == 'DICT':
                self.generate_dict(node)
            elif node[0] == 'DOLLAR':
                self.generate_dollar(node)

        return '\n'.join(self.output)

    def generate_set(self, node):
        name, value = node[1:]
        self.output.append(f"{name} = {self.format_value(value)}")

    def format_value(self, value):
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            return ', '.join([self.format_value(v) for v in value])
        elif isinstance(value, tuple):
            key, val = value
            return f'{key} = {self.format_value(val)}'
        else:
            return str(value)

    def generate_array(self, node):
        items = node[1]
        self.output.append('[')
        for item in items:
            self.output.append(self.format_value(item))
        self.output.append(']')

    def generate_dict(self, node):
        pairs = node[1]
        self.output.append('{')
        for key, value in pairs:
            self.output.append(f'{key} = {self.format_value(value)}')
        self.output.append('}')

    def generate_dollar(self, node):
        var_name = node[1]
        self.output.append(f'${var_name}')