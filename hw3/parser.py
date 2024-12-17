import re

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, text):
        text = self._remove_comments(text)
        text = self._preprocess_constants(text)
        return self._parse_value(text.strip())

    def _remove_comments(self, text):
      """Удаляет однострочные и многострочные комментарии."""
      text = re.sub(r'#.*?\n', '\n', text)
      text = re.sub(r'#\|.*?\|#', '', text, flags=re.DOTALL)
      return text

    def _preprocess_constants(self, text):
        for match in re.finditer(r'set\s+([a-z][a-z0-9_]*)\s*=\s*(.*?);', text):
            name, value_str = match.groups()
            self.constants[name] = self._parse_value(value_str)
        return re.sub(r'set\s+([a-z][a-z0-9_]*)\s*=\s*(.*?);', '', text)

    def _resolve_constants(self, value_str):
      while True:
        match = re.search(r'\$\[([a-z][a-z0-9_]*)\]', value_str)
        if not match:
            break
        name = match.group(1)
        if name in self.constants:
          value_str = value_str.replace(f"$[{name}]", str(self.constants[name]), 1)
        else:
          raise ValueError(f"Undefined constant: {name}")
      return value_str

    def _parse_value(self, text):
        text = self._resolve_constants(text)
        text = text.strip()

        if text.startswith('{'):
          return self._parse_dict(text[1:].strip())
        if text.startswith('array('):
          return self._parse_array(text[6:].strip())

        string_match = re.match(r'"(.*?)"', text)
        if string_match:
            return string_match.group(1)

        try:
           return int(text)
        except ValueError:
           pass

        raise ValueError(f"Invalid value: {text}")


    def _parse_array(self, text):
        if not text.endswith(')'):
             raise ValueError(f"Invalid array syntax {text}")
        text = text[:-1].strip()
        if not text:
           return []

        values = [self._parse_value(item.strip()) for item in text.split(',')]
        return values


    def _parse_dict(self, text):
      if not text.endswith('}'):
        raise ValueError(f"Invalid dictionary syntax {text}")
      text = text[:-1].strip()
      if not text:
          return {}
      items = {}

      # Ищем пары "имя -> значение"
      for match in re.finditer(r'([a-z][a-z0-9_]*)\s*->\s*(.*?)(?=\s*\.\s*([a-z][a-z0-9_]*)\s*->|\s*$)', text):
          name, value_str = match.groups()[:2]
          items[name] = self._parse_value(value_str.strip())
      return items