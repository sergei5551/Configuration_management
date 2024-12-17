import unittest
import os

from hw3.parser import ConfigParser
from hw3.toml_writer import TomlWriter

class TestExamples(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser()
        self.writer = TomlWriter()
        self.output_dir = 'test_output'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
      import shutil
      shutil.rmtree(self.output_dir)

    def test_example_game_config(self):
        config = """
            #Game config
            set version = 1.0;
            {
                title -> "My Awesome Game".
                player_speed -> 5.
                map_size -> array(100,100).
                objects -> {
                    player -> {
                        texture -> "player.png".
                        health -> 100.
                    }.
                    enemy -> {
                        texture -> "enemy.png".
                        damage -> 20.
                    }
                }.
                game_version -> $[version]
            }
        """
        parsed_data = self.parser.parse(config)
        output_file = os.path.join(self.output_dir, 'game_config.toml')
        self.writer.write(parsed_data, output_file)

        expected_data = {
            'title': "My Awesome Game",
            'player_speed': 5,
            'map_size': [100, 100],
            'objects': {
                'player': {
                    'texture': "player.png",
                    'health': 100,
                },
                'enemy': {
                    'texture': "enemy.png",
                    'damage': 20
                }
            },
            'game_version': 1.0
        }

        import toml
        with open(output_file, "r") as f:
             actual_data = toml.load(f)
        self.assertEqual(actual_data, expected_data)


    def test_example_server_config(self):
        config = """
          # Server config
            set port = 8080;
            set max_connections = 100;
            {
                hostname -> "localhost".
                port -> $[port].
                max_connections -> $[max_connections].
                
                database -> {
                    host -> "db.example.com".
                    name -> "mydatabase".
                    user -> "myuser".
                }
            }
        """
        parsed_data = self.parser.parse(config)
        output_file = os.path.join(self.output_dir, 'server_config.toml')
        self.writer.write(parsed_data, output_file)

        expected_data = {
            'hostname': "localhost",
            'port': 8080,
            'max_connections': 100,
            'database': {
                'host': "db.example.com",
                'name': "mydatabase",
                'user': "myuser",
            }
        }

        import toml
        with open(output_file, "r") as f:
             actual_data = toml.load(f)
        self.assertEqual(actual_data, expected_data)

    def test_example_ui_config(self):
        config = """
            #UI Config
            set theme = "dark";
            {
                main_window -> {
                    width -> 800.
                    height -> 600.
                    background_color -> "black".
                    theme -> $[theme].
                   buttons -> array(
                        {
                         id -> "button_1".
                         label -> "Click me"
                         }.
                       {
                         id -> "button_2".
                         label -> "Click me too"
                         }
                    )
                }
             }
        """
        parsed_data = self.parser.parse(config)
        output_file = os.path.join(self.output_dir, 'ui_config.toml')
        self.writer.write(parsed_data, output_file)

        expected_data = {
           'main_window': {
              'width': 800,
              'height': 600,
              'background_color': "black",
              'theme': "dark",
                'buttons' : [
                   {
                    'id': "button_1",
                    'label': "Click me"
                    },
                    {
                    'id': "button_2",
                    'label': "Click me too"
                    }
                ]
           }
        }
        import toml
        with open(output_file, "r") as f:
             actual_data = toml.load(f)
        self.assertEqual(actual_data, expected_data)