#errors
wrong_signature_ = 'Method "%s" already defined in "%s" with a different signature.'
param_wrong_signature = 'Parameter "%s" is already defined in method "%s".'
param_not_exist_ = 'The type of param "%s" in method "%s" not exist, in the class "%s".'
wrong_type_ = 'Type %s expected.'
read_only_ = 'Variable "self" is read-only.'
local_already_defined_ = 'Variable "%s" is already defined in method "%s".'
incompatible_types_ = 'Cannot convert "%s" into "%s".'
var_not_defined_ = 'Variable "%s" is not defined.'
invalid_op_ = 'Operation is not defined between "%s" and "%s".'
incorrect_type_ = 'Incorrect type "%s" waiting "%s".'
autotype_ = 'Cannot infer the type of "%s".'
used_before_assignment_ = 'Variable "%s" used before being assigned.'
circular_dependency_ = 'Circular dependency in "%s".'
b_op_not_defined_ = '%s operations are not defined between "%s" and "%s".'
u_op_not_defined_ = '%s operations are not defined for "%s".'
incorrect_count_params_ = 'Method "%s" of "%s" only accepts "%s" argument(s).'
invalid_SELFTYPE = 'Invalid use of SELF_TYPE.'
self_name = "self cannot be the name of a formal parameter."
self_let_ = "'self' cannot be bound in a 'let' expression."
other_branch_declared_ = 'The type "%s" is declared in another branch.'
attr_not_exist_ = 'The type of attr "%s" in class "%s" not exist.'
invalid_return_type_ = 'The return type "%s" in method "%s" not exist, in the class "%s".'
inherits_builtin_type = 'Type "%s" inherits from a builint type.'
main_method_not_exist_ = 'The main method is not defined in class Main.'
Main_not_defined_ = "The class Main is not defined."

class SemanticException(Exception):
    @property
    def text(self):
        return self.args[0]

class SemanticError():
    def __init__(self,message, line, column, type = 'SemanticError'):
        self.type = type
        self.value = message
        self.line = line
        self.column = column
        self.text = f'({self.line}, {self.column}) - {self.type}: {self.value}'

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.type}: {self.value}'

    def __repr__(self):
        return str(self)
