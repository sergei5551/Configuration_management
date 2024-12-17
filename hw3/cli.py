import sys
from hw3.parser import ConfigParser
from hw3.toml_writer import TomlWriter


def main(output_file):
    config_text = sys.stdin.read()
    try:
        config_parser = ConfigParser()
        data = config_parser.parse(config_text)
        toml_writer = TomlWriter()
        toml_writer.write(data, output_file)
        print(f"Successfully written to {output_file}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
     if len(sys.argv) > 1:
         main(sys.argv[1])
     else:
          print("Error: output file path is required as an argument")
          sys.exit(1)