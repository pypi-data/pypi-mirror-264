import ast


class OneLetterVariableChecker(object):
    name = "flake8_one_letter_variables_check"
    version = "0.0.1"
    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                variable_name = node.id
                if len(variable_name) == 1:
                    error_message = f"OLV001 DO NOT USE ONE LETTER VARIABLE: variable name '{variable_name}'"
                    yield node.lineno, node.col_offset, error_message, type(self)
