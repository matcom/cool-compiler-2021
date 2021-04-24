from cool.error.errors import SemanticError,RunError, NO_OPERATION_DEFINDED, MULTIPLE_OPERATION_DEFINED, ZERO_DIVISION
from cool.ast.ast import * 
from cool.semantic.type import *
from cool.semantic.atomic import *

class Operator:
    
    def __init__(self,context,errors):
        object_type = context.get_type('Object')
        int_type = context.get_type('Int')
        string_type = context.get_type('String')
        bool_type = context.get_type('Bool')
        void_type = context.get_type('Void')
        self.operations = OperationDict({
            ('~',(int_type,)):(lambda x: ClassInstance(int_type,context,self,errors,value=-x.value),int_type),
            ('-',(int_type,int_type)):(lambda x,y:   ClassInstance(int_type,context,self,errors,value=x.value -  y.value),int_type),
            ('+',(int_type,int_type)):(lambda x,y:   ClassInstance(int_type,context,self,errors,value=x.value +  y.value),int_type),
            ('*',(int_type,int_type)):(lambda x,y:   ClassInstance(int_type,context,self,errors,value=x.value *  y.value),int_type),
            ('/',(int_type,int_type)):(lambda x,y:   ClassInstance(int_type,context,self,errors,value=x.value // y.value),int_type),
            ('<' ,(int_type,int_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value <  y.value),bool_type),
            ('>' ,(int_type,int_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value >  y.value),bool_type),
            ('<=',(int_type,int_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value <= y.value),bool_type),
            ('>=',(int_type,int_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value >= y.value),bool_type),
            ( '=',(int_type,int_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value == y.value),bool_type),

            ('<' ,(string_type,string_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value <  y.value),bool_type),
            ('>' ,(string_type,string_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value >  y.value),bool_type),
            ('<=',(string_type,string_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value <= y.value),bool_type),
            ('>=',(string_type,string_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value >= y.value),bool_type),
            ( '=',(string_type,string_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value == y.value),bool_type),

            ('not',(bool_type,)):(lambda x: ClassInstance(bool_type,context,self,errors,value=not x.value),bool_type),
            ( '=',(bool_type,bool_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.value == y.value),bool_type),
            
            ('isvoid',(object_type,)):(lambda x: ClassInstance(bool_type,context,self,errors,value=x.type == void_type),bool_type),
            
            ( '=',(object_type,object_type)):(lambda x,y: ClassInstance(bool_type,context,self,errors,value=x.scope.get_variable_value('self') == y.scope.get_variable_value('self')),bool_type),
        })
        self.operator = {
            PlusNode:'+',
            MinusNode:'-',
            DivNode:'/',
            StarNode:'*',
            NotNode:'not',
            GreaterEqualNode:'>=',
            GreaterNode:'>',
            LesserEqualNode:'<=',
            LesserNode:'<',
            EqualNode:'=',
            RoofNode:'~',
            IsVoidNode:'isvoid',
        }        
    
    def register_operation(self,operator,function,return_type,*types):
        self.operations[operator,types] = (function,return_type)
    
    def get_operator(self,node):
        return self.operator.get(type(node),None)
    
    def operation_defined(self,node, *types):
        operator = self.get_operator(node)
        if operator:
            return (operator,types) in self.operations
        return False
    
    def type_of_operation(self,node,*types):
        operator = self.get_operator(node)
        if operator:
            try:
                value = self.operations[(operator,types)]
            except KeyError:
                return ErrorType()
            return value[1]
        return ErrorType()
    
    def operate(self,operator,*values):
        types = tuple(value.type for value in values)
        try:
            return self.operations[operator,types][0](*values)
        except KeyError as exc:
            raise RunError(exc.args[0])
        except ZeroDivisionError as exc:
            raise RunError(ZERO_DIVISION)
        
    def __str__(self):
        return str(self.operations)
        
class OperationDict:
    def __init__(self, default:"(operator,*types)->(func_operator,return_type)"={}):
        self.operations = default
    
    def get_valid_operators_of(self, operator):
        valid_operators_types = [args for op,args in self.operations if op == operator]
        return valid_operators_types
    
    def get(self,key,default=None):
        operator, types = key
        types = list(types)
        auto_type_index = [i for i,x in enumerate(types) if isinstance(x, AutoType)]
        if not auto_type_index:
            try:
                return self[key]
            except KeyError:
                return default
            
        possible_operations_types = [oper_types for oper,oper_types in self.operations if oper == operator and len(oper_types) == len(types)]
        for i in [i for i in range(len(types)) if i not in auto_type_index]:
            possible_operations_types = [x for x in possible_operations_types if x[i] == types[i]]
        
        combinations = dict()
        for i, possibles in [(i, types[i].possibles) for i in auto_type_index]:
            no_possibles = []
            for possible in possibles:
                if any(x for x in possible_operations_types if x[i] == possible):
                    value = combinations.get(i,[])
                    value.append(possible)
                    combinations[i] = value
                else:
                    no_possibles.append(possible)
            for to_remove in no_possibles:
                types[i].remove_possible(to_remove)
                
        if len(combinations) != len(auto_type_index):
            raise KeyError("No operation can satisfy the current types")        
        
        results = []
        import cool.visitors.utils as ut
        for possible_types in ut.set_permutation(*[combinations[i] for i in auto_type_index]):
            type_key = [x for x in types]
            for j,i in enumerate(auto_type_index):
                type_key[i] = possible_types[j]
            type_key = tuple(type_key)
            try:
                result = self[operator,type_key]
                results.append(result) 
            except KeyError:
                for j,i in enumerate(auto_type_index):
                    types[i].remove_possible(possible_types[j])
            
        if len(results) != 1:
            raise KeyError("Result must have a cardinality of 1")
        return results[0]
    
    def get_covariant(self,key):
        operator,types = key
        possible_op = []
        
        for op,op_types in self.operations:
            if operator == op and len(types) == len(op_types):
                for op_type,key_type in zip(op_types,types):
                    if not (op_type in key_type.get_parents() or op_type == key_type):
                        break
                else:
                    possible_op.append((op,op_types)) 
        
        if len(possible_op) > 1:
            raise KeyError(MULTIPLE_OPERATION_DEFINED.format(operator,types))
        if len(possible_op) == 0:
            raise KeyError(NO_OPERATION_DEFINDED.format(operator, types))
        
        return self.operations[possible_op[0]]
    
    def __getitem__(self,key):
        operator,types = key
        try:
            return self.operations[key]
        except KeyError:
            if any(x for x in key[1] if isinstance(x,AutoType)):
                result = self.get(key)
                return result
                raise KeyError(NO_OPERATION_DEFINDED.format(operator, types))
            return self.get_covariant(key)
        except TypeError: # Unhashable error
            raise KeyError(NO_OPERATION_DEFINDED.format(operator, types))
    
    def __contains__(self,key):
        try:
            self[key]
            return True
        except KeyError:
            return False
    
    def __setitem__(self,key,value):
        op,types = key
        self.operations[key] = value
        
    def __str__(self):
        return "\n".join([f"{op} : {', '.join([typex.name for typex in types])} --> {ret_type.name}" for (op, types),(func, ret_type) in self.operations.items()])