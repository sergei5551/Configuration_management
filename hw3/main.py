import sys
import my_parser
from toml_generator import TomlGenerator

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as file:
        data = file.read()

    try:
        ast = my_parser.parse(data)
        generator = TomlGenerator(ast)
        toml_code = generator.generate()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    with open(output_file, 'w') as file:
        file.write(toml_code)

    print(f"Configuration successfully converted to TOML and saved to {output_file}.")