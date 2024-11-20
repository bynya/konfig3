import argparse
import json
import re

class ConfigParser:
    def __init__(self):
        self.variables = {}

    def parse(self, config_text):
        lines = config_text.splitlines()
        buffer = ""
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.endswith(";") and not buffer:
                self._parse_variable_declaration(line)
            else:
                buffer += line
                if buffer.endswith(";"):
                    self._parse_variable_declaration(buffer)
                    buffer = ""
        if buffer:
            raise SyntaxError(f"Incomplete declaration: {buffer}")

    def _parse_variable_declaration(self, line):
        match = re.match(r"var ([A-Z_][A-Z0-9_]*) := (.+);", line)
        if not match:
            raise SyntaxError(f"Invalid variable declaration: {line}")
        name, value = match.groups()
        self.variables[name] = self._parse_value(value)

    def _parse_value(self, value):
        value = value.strip()
        if value.startswith("(") and value.endswith(")"):
            if value == "()":
                return []
            return self._parse_array(value)
        elif value.startswith("{") and value.endswith("}"):
            if value == "{}":
                return {}
            return self._parse_dict(value)
        elif value.startswith("$") and value.endswith("$"):
            return self._evaluate_expression(value[1:-1])
        elif value.isdigit():
            return int(value)
        elif value in self.variables:
            return self.variables[value]
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        else:
            raise SyntaxError(f"Invalid value: {value}")

    def _parse_array(self, value):
        content = value[1:-1].strip()
        elements = []
        buffer = ""
        depth = 0

        for char in content:
            if char in "{(":
                depth += 1
            elif char in "})":
                depth -= 1
            if char == "," and depth == 0:
                elements.append(buffer.strip())
                buffer = ""
            else:
                buffer += char
        if buffer:
            elements.append(buffer.strip())

        return [self._parse_value(el) for el in elements]

    def _parse_dict(self, value):
        content = value[1:-1].strip()
        items = []
        buffer = ""
        depth = 0

        for char in content:
            if char in "{(":
                depth += 1
            elif char in "})":
                depth -= 1
            if char == "," and depth == 0:
                items.append(buffer.strip())
                buffer = ""
            else:
                buffer += char
        if buffer:
            items.append(buffer.strip())

        result = {}
        for item in items:
            if "=>" not in item:
                raise SyntaxError(f"Invalid dictionary item: {item}")
            key, val = item.split("=>", 1)
            result[key.strip()] = self._parse_value(val.strip())
        return result

    def _evaluate_expression(self, expression):
        tokens = expression.split()
        operator = tokens[0]
        if operator == "+":
            return sum(int(self._get_value(t)) for t in tokens[1:])
        if operator == "mod":
            if len(tokens) != 3:
                raise ValueError("mod() requires exactly two arguments.")
            return int(self._get_value(tokens[1])) % int(self._get_value(tokens[2]))
        raise ValueError(f"Unknown operator: {operator}")

    def _get_value(self, token):
        if token.isdigit():
            return int(token)
        if token in self.variables:
            return self.variables[token]
        raise ValueError(f"Unknown variable: {token}")

    def _evaluate_structure(self, structure):
        if isinstance(structure, list):
            return [self._evaluate_structure(item) for item in structure]
        if isinstance(structure, dict):
            return {key: self._evaluate_structure(value) for key, value in structure.items()}
        if isinstance(structure, str) and structure.startswith("$") and structure.endswith("$"):
            return self._evaluate_expression(structure[1:-1])
        return structure


def main():
    parser = argparse.ArgumentParser(description="Config language to JSON converter")
    parser.add_argument("--input", required=True, help="Path to the input config file")
    parser.add_argument("--output", required=True, help="Path to the output JSON file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        config_text = f.read()

    config_parser = ConfigParser()
    config_parser.parse(config_text)

    evaluated_data = config_parser._evaluate_structure(config_parser.variables)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(evaluated_data, f, indent=2)
    print(f"Запись сохранена в {args.output}")


if __name__ == "__main__":
    main()
