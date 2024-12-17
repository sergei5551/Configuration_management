import unittest
from hw3.parser import ConfigParser


class TestParser(unittest.TestCase):

  def test_remove_comments(self):
    parser = ConfigParser()
    text = """
    # this is a comment
    #|
    This is a 
    multiline comment
    |#
    value
    """

    expected = """
    
    
    value
    """

    self.assertEqual(parser._remove_comments(text), expected)

  def test_parse_number(self):
        parser = ConfigParser()
        self.assertEqual(parser.parse("123"), 123)

  def test_parse_array(self):
        parser = ConfigParser()
        self.assertEqual(parser.parse("array(1,2,3)"), [1, 2, 3])
        self.assertEqual(parser.parse("array( 1, 2,3 )"), [1, 2, 3])
        self.assertEqual(parser.parse("array(  )"), [])
  def test_parse_nested_array(self):
        parser = ConfigParser()
        self.assertEqual(parser.parse("array(1,array(2,3),4)"), [1, [2, 3], 4])

  def test_parse_dict(self):
    parser = ConfigParser()
    self.assertEqual(parser.parse("{a -> 1 . b -> 2 . c -> 3}"), {'a': 1, 'b': 2, 'c': 3})
    self.assertEqual(parser.parse("{ a -> 1 . b -> 2 . c -> 3 }"), {'a': 1, 'b': 2, 'c': 3})
    self.assertEqual(parser.parse("{   }"), {})
  def test_parse_nested_dict(self):
      parser = ConfigParser()
      self.assertEqual(parser.parse("{a -> 1 . b -> {c -> 2 }}"), {'a': 1, 'b': {'c': 2}})


  def test_parse_set_constant(self):
        parser = ConfigParser()
        parser.parse("set x = 123;")
        self.assertEqual(parser.constants, {"x": 123})


  def test_resolve_constant(self):
     parser = ConfigParser()
     parser.constants = {"x": 10, "y": 20}
     self.assertEqual(parser._resolve_constants("$[x]"), "10")
     self.assertEqual(parser._resolve_constants("value $[x]"), "value 10")
     self.assertEqual(parser._resolve_constants("$[y]  $[x]"), "20  10")
     self.assertEqual(parser._resolve_constants(" $[x] + $[y]"), " 10 + 20")

  def test_parse_constant_expression(self):
        parser = ConfigParser()
        parser.parse("set x = 10; set y = 20;")
        self.assertEqual(parser.parse("$[x]"), 10)
        self.assertEqual(parser.parse("array($[x], $[y])"), [10, 20])
        self.assertEqual(parser.parse("{ a -> $[x] . b -> $[y] }"), {'a': 10, 'b': 20})

  def test_parse_mixed(self):
        parser = ConfigParser()
        config = """
        set version = 1;
        set array_size = 3;
        {
            app_version -> $[version].
            data -> array(1,2, array($[array_size],4), {name -> "test"})
        }
        """

        expected = {'app_version': 1, 'data': [1, 2, [3, 4], {'name': 'test'}]}
        self.assertEqual(parser.parse(config), expected)

  def test_parse_errors(self):
        parser = ConfigParser()
        with self.assertRaisesRegex(ValueError, "Invalid array syntax"):
           parser.parse("array(1,2")
        with self.assertRaisesRegex(ValueError, "Invalid dictionary syntax"):
           parser.parse("{a -> 1")
        with self.assertRaisesRegex(ValueError, "Invalid dictionary item"):
           parser.parse("{ a 1 }")
        with self.assertRaisesRegex(ValueError, "Undefined constant"):
           parser.parse("$[unknown]")
        with self.assertRaisesRegex(ValueError, "Invalid value"):
          parser.parse("invalid")