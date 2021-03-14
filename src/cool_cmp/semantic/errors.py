"""
Semantic errors
"""

from cool_cmp.shared.errors import CoolError

VARIABLE_ALREADY_DEFINED = lambda variable_name: f"Variable {variable_name} already defined"
VARIABLE_NOT_DEFINED = lambda variable_name: f"Variable {variable_name} is not defined"
METHOD_ALREADY_DEFINED = lambda method_name, param_count, type_name: f"Method {method_name} with {param_count} params already defined in {type_name}"
METHOD_REDEFINITION_INVALID = lambda method_name, old_signature: f"Method {method_name} already defined with {old_signature} in a parent class" 
METHOD_NOT_DEFINED = lambda method_name, params_count, type_name: f"Method {method_name} with {params_count} params is not defined in {type_name}"
ATTRIBUTE_ALREADY_DEFINED = lambda attribute_name, type_name: f"Attribute {attribute_name} already defined in {type_name}"
ATTRIBUTE_NOT_DEFINED = lambda attr_name, type_name: f"Attribute {attr_name} not defined in {type_name}"
TYPE_NOT_DEFINED = lambda type_name: f"Type {type_name} not defined"
TYPE_ALREADY_DEFINED = lambda type_name: f"Type {type_name} already defined"
TYPE_NOT_INHERITABLE = lambda type_name: f"Can't inherit from {type_name}"

class SemanticError(CoolError):
    """
    Base Semantic Error
    """
    pass

