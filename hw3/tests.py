import unittest
from main import parse_and_generate_toml

class TestConfigParser(unittest.TestCase):
    def test_simple_set(self):
        input_data = """
        set a = 10;
        """
        expected_output = """a = 10"""
        actual_output = parse_and_generate_toml(input_data)
        self.assertEqual(actual_output, expected_output)

    def test_array(self):
        input_data = """
        set arr = [1, 2, 3];
        """
        expected_output = """arr = [1, 2, 3]"""
        actual_output = parse_and_generate_toml(input_data)
        self.assertEqual(actual_output, expected_output)

    def test_dict(self):
        input_data = """
        set d = {
            key1 -> "value1",
            key2 -> 42,
            key3 -> [1, 2, 3],
        };
        """
        expected_output = """d = { key1 = "value1", key2 = 42, key3 = [1, 2, 3] }"""
        actual_output = parse_and_generate_toml(input_data)
        self.assertEqual(actual_output, expected_output)

    def test_nested_structures(self):
        input_data = """
        set nested = {
            inner_arr -> [1, 2, 3],
            inner_dict -> {
                key1 -> "value1",
                key2 -> 42,
            },
        };
        """
        expected_output = """nested = { inner_arr = [1, 2, 3], inner_dict = { key1 = "value1", key2 = 42 } }"""
        actual_output = parse_and_generate_toml(input_data)
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()