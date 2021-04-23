from cool_cmp.semantic.implementations import CoolType, SemanticError, VariableInfo
import pytest

# To execute the test $ pytest src/cool_cmp/semantic/tests/

def test_type_attribute():
    """
    Attribute Redefinition in same type
    """
    obj = CoolType("Object", None)
    attr = obj.add_attribute("a", obj)
    with pytest.raises(SemanticError):
        obj.add_attribute("a", obj)


def test_type_attribute_2():
    """
    Attribute Redefinition in child type
    """
    obj = CoolType("Object", None)
    attr = obj.add_attribute("a", obj)
    obj2 = CoolType("Object2", obj)
    with pytest.raises(SemanticError):
        obj2.add_attribute("a", obj2)


def test_type_method():
    """
    Method Definition with same signature
    """
    obj = CoolType("Object", None)
    attr = obj.add_method("a", [VariableInfo("a", obj)], obj)
    with pytest.raises(SemanticError):
        obj.add_method("a", [VariableInfo("b", obj)], obj)


def test_type_method_2():
    """
    Method Definition with same params names
    """
    obj = CoolType("Object", None)
    with pytest.raises(SemanticError):
        attr = obj.add_method("a", [VariableInfo("a", obj), VariableInfo("a", obj)], obj)

