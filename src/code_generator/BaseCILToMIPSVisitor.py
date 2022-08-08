
class BaseCILToMIPSVisitor:
    def __init__(self):
        self.mips_code = ''
        self.text = ''
        self.data = ''
        self.mips_operators = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            '<': 'slt',
            '<=': 'sle',
            '=': 'seq',
        }
        self.current_function = None
        self.types = None
        self.attr_offset = {}
        self.method_offset = {}
        self.var_offset = {}
        self.runtime_errors = {}
        self.register_runtime_errors()

    def is_param(self, name):
        return name in self.current_function.params

    def register_runtime_errors(self):
        self.runtime_errors[
            'dispatch_void'] = 'Runtime Error: A dispatch (static or dynamic) on void'
        self.runtime_errors['case_void'] = 'Runtime Error: A case on void'
        self.runtime_errors['case_no_match'] = 'Runtime Error: Execution of a case statement without a matching branch'
        self.runtime_errors['div_zero'] = 'Runtime Error: Division by zero'
        self.runtime_errors['substr'] = 'Runtime Error: Substring out of range'
        self.runtime_errors['heap'] = 'Runtime Error: Heap overflow'
        for error in self.runtime_errors:
            self.data += f'{error}: .asciiz "{self.runtime_errors[error]}"\n'
            self.generate_runtime_error(error)

    def generate_runtime_error(self, error):
        self.text += f'{error}_error:\n'
        self.text += f'la $a0 {error}\n'
        self.text += f'li $v0, 4\n'
        self.text += 'syscall\n'
        self.text += 'li $v0, 10\n'
        self.text += 'syscall\n'
