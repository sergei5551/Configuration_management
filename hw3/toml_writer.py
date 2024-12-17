import toml


class TomlWriter:
    def write(self, data, file_path):
        with open(file_path, 'w') as f:
            toml.dump(data, f)