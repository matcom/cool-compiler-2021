"""
Semantic errors
"""

from cool_cmp.shared.errors import CoolError

VARIABLE_ALREADY_DEFINED = lambda variable_name: f"Variable {variable_name} already defined"
VARIABLE_NOT_DEFINED = lambda variable_name: f"Variable {variable_name} is not defined"
METHOD_PARAMS_NAMES_EQUALS = lambda method_name: f"Params with equal names present in {method_name}"
METHOD_ALREADY_DEFINED = lambda method_name, param_count, type_name: f"Method {method_name} with {param_count} params already defined in {type_name}"
METHOD_REDEFINITION_INVALID = lambda method_name, old_signature: f"Method {method_name} already defined with {old_signature} in a parent class" 
METHOD_NOT_DEFINED = lambda method_name, params_count, type_name: f"Method {method_name} with {params_count} params is not defined in {type_name}"
ATTRIBUTE_ALREADY_DEFINED = lambda attribute_name, type_name: f"Attribute {attribute_name} already defined in {type_name}"
ATTRIBUTE_NOT_DEFINED = lambda attr_name, type_name: f"Attribute {attr_name} not defined in {type_name}"
TYPE_NOT_DEFINED = lambda type_name: f"Type {type_name} not defined"
TYPE_ALREADY_DEFINED = lambda type_name: f"Type {type_name} already defined"
TYPE_NOT_INHERITABLE = lambda type_name: f"Can't inherit from {type_name}"
TYPE_CYCLIC_DEPENDENCY = lambda cycle: f"Types {', '.join(cycle)} form a cyclic dependency"

class SemanticError(CoolError):
    """
    Base Semantic Error
    """
    
    ERROR_TYPE = "SemanticError"

    FORMAT = "({}, {}) - {}: {}"

    def set_position(self, line:int, col:int):
        """
        Set the line and column of this error
        """
        self.line = line
        self.column = col

    def __str__(self):
        if hasattr(self, 'line') and hasattr(self, 'column'):
            return self.FORMAT.format(self.line, self.column, self.ERROR_TYPE, self.error)
        return self.ERROR_TYPE + " - " + self.error


