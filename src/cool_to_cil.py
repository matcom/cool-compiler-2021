import visitor as visitor
from AST import *
import AST_CIL, basic_classes

class Build_CIL:
    def __init__(self, ast, sem):
        self.end_line = {}
        self.info = sem
        self.current_method = None
        self.const_1 = 'const_1'
        self.null_const = 'const_0'
        self.idCount = 0
        self.astCIL = AST_CIL.Program()
        self._self = Var('self', 'SELF_TYPE')
        self._self.line = 0
        self._self.index = 0
        self.local_variables = [self._self]
        self.constructor = {}
        self.classmethods = {}
        self.class_functions_list = {}
        self.class_attrs = {}
        for item in sem.class_attrs.items():
            self.class_attrs[item[0]] = [x.id for x in item[1]]
        
        self.BFS(sem.graph, sem.classmethods_original, sem.classmethods)
        self.compute_function_list(sem.classmethods_original, sem.graph)
                
        self.visit(ast, self.astCIL)

    def BFS(self, graph, class_methods_original, inherits_methods):
        self.classmethods[('Object', 'abort')]        = 'function_Object_abort'
        self.classmethods[('Object', 'type_name')]    = 'function_Object_type_name'
        self.classmethods[('Object', 'copy')]         = 'function_Object_copy'
        self.classmethods[('IO', 'out_string')]       = 'function_IO_out_string'
        self.classmethods[('IO', 'out_int')]          = 'function_IO_out_int'
        self.classmethods[('IO', 'in_string')]        = 'function_IO_in_string'
        self.classmethods[('IO', 'in_int')]           = 'function_IO_in_int'
        self.classmethods[('String', 'length')]       = 'function_String_length'
        self.classmethods[('String', 'concat')]       = 'function_String_concat'
        self.classmethods[('String', 'substr')]       = 'function_String_substr'
        for c, methods in class_methods_original.items():
            for m in methods:
                self.classmethods[(c, m)] = 'function_' + c + '_' + m

        l = ['Object']
        while len(l) > 0:
            temp = l.pop(0)
            if not graph.__contains__(temp): continue
            for _class in graph[temp]:
                l.append(_class)
                for function in inherits_methods[temp]:
                    if self.classmethods.__contains__((_class, function)): continue
                    self.classmethods[(_class, function)] = self.classmethods[(temp, function)]

    def compute_function_list(self, class_methods_original, graph):
        for c, methods in class_methods_original.items():
            for m in methods:
                fname = 'function_' + c + '_' + m
                if not self.class_functions_list.__contains__(c):
                    self.class_functions_list[c] = []
                self.class_functions_list[c].append(fname)

        l = ['Object']
        while len(l) > 0:
            
            temp = l.pop(0)
            
            if not graph.__contains__(temp): continue
            
            for _class in graph[temp]:
                
                l.append(_class)
                index = 0
                if not self.class_functions_list.__contains__(_class):
                    self.class_functions_list[_class] = []
                
                for function in self.class_functions_list[temp]:        #lista de funciones de parent
                    
                    k = len(temp)
                    end = len(function)
                    fname = 'function_' + _class + '_' + function[10 + k : end]     

                    if self.class_functions_list[_class].__contains__(fname):
                        self.class_functions_list[_class].remove(fname)
                        self.class_functions_list[_class].insert(index, fname)                      #is a original function 
                    else:
                        self.class_functions_list[_class].insert(index, function)                   #is a inherit function 

                    index += 1

    def get_local(self):
        dest = 'local_' + str(self.idCount)
        self.idCount += 1
        return dest

    def get_label(self):
        label = 'label' + str(self.idCount)
        self.idCount+=1
        return label

    @visitor.on('node')
    def visit(self, node, nodeCIL):
        pass

    @visitor.when(Program)
    def visit(self, program, programCIL):

        basic_classes.Build(self.astCIL.code_section, self.astCIL.type_section)
        func = 'main'
        f = AST_CIL.Function(func)

        self_instance = 'self'          #crear instancia de un valor entero
        false_local = 'false'

        intr  = AST_CIL.Call(self_instance, 'function_Main___init__')

        intr2 = AST_CIL.Arg(self_instance)
        intr3 = AST_CIL.Call(false_local, 'function_Main_main')
        intr4 = AST_CIL.Exit()
        
        f.instructions += [intr, intr2, intr3, intr4]
        f.localvars += [false_local, self_instance]
        self.astCIL.code_section.insert(0, f)
        
        for c in program.classes:
            self.visit(c, programCIL)

    @visitor.when(Class)
    def visit(self, _class, programCIL):

        #clase que estoy visitando
        self.current_class = _class.name

        #crear el tipo correspondiente
        _type = AST_CIL.Type(_class.name)
        self.current_method = None
        func = 'function' + '_' + self.current_class + '_' + '__init__'     #   --->   devuelve una instancia de la clase
        _type.methods ['__init__'] = func                                   #   --->   añado el metodo init a la clase
        f = AST_CIL.Function(func)

        self_instance = 'self'                                              #   --->  reservo espacio en el heap para self
        intr = AST_CIL.Allocate(self_instance, _class.name)                 #   --->  reservo para la cant de atributos del Main

        #f.instructions.append(intr)
        f.localvars += [self_instance]

        #################################
        #visito los atributos
        index = 0
        for att in _class.attributes:
            
            attribute_instance = self.visit(att, f)
            
            _intr = AST_CIL.SetAttrib(self_instance, index, attribute_instance)
            
            #f.instructions.insert(1, _intr)    #<------cambio
            f.instructions.append(_intr)        #<------comment
            
            index += 1
        #################################

        f.instructions.insert(0, intr)

        f.instructions.append(AST_CIL.Return(self_instance))

        ##########################################
        local = self.const_1
        intr1 = AST_CIL.Allocate(local, 'Int')
        intr2 = AST_CIL.SetAttrib(local, 0, 1)
        f.instructions.insert(0, intr2)
        f.instructions.insert(0, intr1)
        f.localvars.append(local)

        local2 = self.null_const
        intr3 = AST_CIL.Allocate(local2, 'Int')
        intr4 = AST_CIL.SetAttrib(local2, 0, 0)
        f.instructions.insert(0, intr4)
        f.instructions.insert(0, intr3)
        f.localvars.append(local2)   
        #########################################

        self.astCIL.code_section.append(f)

        #visito los metodos
        for m in _class.methods: self.visit(m, _type)
        programCIL.type_section.append(_type)
        self.current_class = None

    @visitor.when(Method)
    def visit(self, method, typeCIL):
        self.current_method = method.id
        func = 'function' + '_' + self.current_class + '_' + method.id
        typeCIL.methods[method.id] = func
        f = AST_CIL.Function(func)
        f.params.insert(0, 'self')

        for arg in method.parameters:
            f.params.append(arg.id)        

        result = self.visit(method.expression, f)

        f.instructions.append(AST_CIL.Return(result))

        ##########################################
        local = self.const_1
        intr = AST_CIL.Allocate(local, 'Int')
        intr2 = AST_CIL.SetAttrib(local, 0, 1)
        f.instructions.insert(0, intr2)
        f.instructions.insert(0, intr)
        f.localvars.append(local)

        local2 = self.null_const
        intr3 = AST_CIL.Allocate(local2, 'Int')
        intr4 = AST_CIL.SetAttrib(local2, 0, 0)
        f.instructions.insert(0, intr4)
        f.instructions.insert(0, intr3)
        f.localvars.append(local2)   
        #########################################     

        self.astCIL.code_section.append(f)
        self.local_variables.clear()
        self.local_variables.append(self._self)
        self.current_method = None

    @visitor.when(Boolean)
    def visit(self, _bool, functionCIL):
        instance = self.get_local()
        intr1 = AST_CIL.Allocate(instance, 'Bool')
        value = 0
        if _bool.value == 'true': value = 1
        intr2 = AST_CIL.SetAttrib(instance, 0, value)
        functionCIL.localvars.append(instance)
        functionCIL.instructions.insert(0, intr2)
        functionCIL.instructions.insert(0, intr1)
        return instance

    @visitor.when(Interger)
    def visit(self, _int, functionCIL):
        instance = self.get_local()
        intr1 = AST_CIL.Allocate(instance, 'Int')
        intr2 = AST_CIL.SetAttrib(instance, 0, _int.value)
        functionCIL.localvars.append(instance)
        functionCIL.instructions.insert(0, intr2)
        functionCIL.instructions.insert(0, intr1)
        return instance

    @visitor.when(NewType)
    def visit(self, _newType, functionCIL):
        instance = self.get_local()
        intr1 = AST_CIL.Allocate(instance, _newType.type_name)

        if _newType.type_name == 'Int' or _newType.type_name == 'Bool':
            intr2 = AST_CIL.SetAttrib(instance, 0, 0)            
            functionCIL.instructions.insert(0, intr2)
        
        elif not _newType.type_name  == 'IO' and not _newType.type_name  == 'Object' and not _newType.type_name  == 'String':
            intr3 = AST_CIL.Call(instance, 'function_' + _newType.type_name + '_' + '__init__')
            functionCIL.instructions.append(intr3)

        functionCIL.localvars.append(instance)
        functionCIL.instructions.insert(0, intr1)
        return instance

    @visitor.when(String)
    def visit(self, string, functionCIL):
        tag = 's' + str(len(self.astCIL.data_section))
        n = len(string.value)
        if n > 0 and string.value.__contains__('\n'):       #[n-1] == '\n':
            s = string.value.replace("\n", '\\n')
            s = '\"' + s + '\"'
        else: s = '"' + string.value + '"'

        # self.astCIL.data_section[s] = tag
        if self.astCIL.data_section.__contains__(s):
            tag = self.astCIL.data_section[s]
        else: self.astCIL.data_section[s] = tag

        instance = self.get_local()
        intr1 = AST_CIL.Allocate(instance, 'String')
        intr2 = AST_CIL.Load(instance, tag)

        functionCIL.localvars.append(instance)
        functionCIL.instructions.insert(0, intr2)
        functionCIL.instructions.insert(0, intr1)
        return instance

    @visitor.when(StaticDispatch)
    def visit(self, static_dispatch, functionCIL):
        dest = 'local_' + str(self.idCount)
        self.idCount += 1

        args_list = []
        for item in static_dispatch.parameters: args_list.append(self.visit(item, functionCIL))

        result = self.visit(static_dispatch.left_expression, functionCIL)

        functionCIL.instructions.append(AST_CIL.Arg(result))        #Bind self

        for item in args_list: functionCIL.instructions.append(AST_CIL.Arg(item))

        intr = AST_CIL.Call(dest, self.classmethods[(static_dispatch.parent_type, static_dispatch.func_id)])
        #intr = AST_CIL.Dynamic_Call(dest, static_dispatch.left_expression.static_type, self.classmethods[(static_dispatch.left_expression.static_type, static_dispatch.func_id)], result)

        functionCIL.localvars.append(dest)

        functionCIL.instructions.append(intr)

        return dest

    @visitor.when(Dispatch)
    def visit(self, dispatch, functionCIL):
        dest = 'local_' + str(self.idCount)
        self.idCount += 1
        args_list = []
        for item in dispatch.parameters: args_list.append(self.visit(item, functionCIL))
        if dispatch.left_expression is None:
            functionCIL.instructions.append(AST_CIL.Arg('self'))
            for item in args_list: functionCIL.instructions.append(AST_CIL.Arg(item))
            
            #intr = AST_CIL.Call(dest, self.classmethods[(self.current_class, dispatch.func_id)])
            intr = AST_CIL.Dynamic_Call(dest, self.current_class, self.classmethods[(self.current_class, dispatch.func_id)], 'self')
            
            functionCIL.localvars.append(dest)
            functionCIL.instructions.append(intr)
        
        else:            
            result = self.visit(dispatch.left_expression, functionCIL)

            functionCIL.instructions.append(AST_CIL.Arg(result))        #Bind self

            for item in args_list: functionCIL.instructions.append(AST_CIL.Arg(item))

            #intr = AST_CIL.Call(dest, self.classmethods[(dispatch.left_expression.static_type, dispatch.func_id)])
            intr = AST_CIL.Dynamic_Call(dest, dispatch.left_expression.static_type, self.classmethods[(dispatch.left_expression.static_type, dispatch.func_id)], result)

            functionCIL.localvars.append(dest)
            functionCIL.instructions.append(intr)
        return dest

    @visitor.when(Block)
    def visit(self, block, functionCIL):
        n = len(block.expressions) - 1
        for i in range(n): self.visit(block.expressions[i], functionCIL)
        result = self.visit(block.expressions[n], functionCIL)
        return result

    @visitor.when(LetVar)
    def visit(self, let, functionCIL):
        for item in let.declarations:
            self.visit(item, functionCIL)
            self.local_variables.append(item)
        result = self.visit(let.in_expression, functionCIL)

        n = len(let.declarations)        
        m = len(self.local_variables)        
        for i in range(n): self.local_variables.pop(m - i - 1)
        return result

    @visitor.when(Attribute)#ok
    def visit(self, attr, functionCIL):
       
        #declara un nuevo objeto y le asigna un valor
       
        result = self.visit(attr.expr, functionCIL)
       
        instance = attr.id + '_' + str(attr.line) + '_' + str(attr.index)        #creo una instancia con el nombre del atributo

        #intr1 = AST_CIL.Allocate(instance, attr.type)          # <--------- change
        #functionCIL.instructions.insert(0, intr1)              # <--------- change
        #intr2 = AST_CIL.Assign(instance, attr.type, result)    # <--------- change

        #change-------------------------------------------------------------------
        
        intr2 = AST_CIL.Copy(instance, result)

        # ---> poner los atributos en su indice
        functionCIL.localvars.append(instance)
        
        functionCIL.instructions.append(intr2)

        return instance

    @visitor.when(Var)
    def visit(self, var, functionCIL): #expr --> ID : TYPE
        #declara un nuevo objeto y le asigna un valor inicial
        instance =  var.id + '_' + str(var.line) + '_' + str(var.index)
        intr1 = AST_CIL.Allocate(instance, var.type)

        if var.type == 'Int' or var.type == 'Bool':
            intr2 = AST_CIL.SetAttrib(instance, 0, 0)
            functionCIL.instructions.insert(0, intr2)
            
        elif var.type == 'String':
            tag = 's' + str(len(self.astCIL.data_section))
            s = '""'
            # self.astCIL.data_section[s] = tag
            if self.astCIL.data_section.__contains__(s):
                tag = self.astCIL.data_section[s]
            else: self.astCIL.data_section[s] = tag

            intr1 = AST_CIL.Allocate(instance, 'String')
            intr2 = AST_CIL.Load(instance, tag)
            functionCIL.instructions.insert(0, intr2)

        functionCIL.localvars.append(instance)
        functionCIL.instructions.insert(0, intr1)
        return instance

    @visitor.when(Type)     #expr --> ID
    def visit(self, _type, functionCIL):
        if _type.name == 'self': return 'self'
        n = len(self.local_variables) - 1

        #variable local(let, case) ok
        for i in range(n, -1, -1):
            local_id =  self.local_variables[i].id
            if local_id == _type.name:
                return local_id + '_' + str(self.local_variables[i].line) + '_' + str(self.local_variables[i].index)

        #parametro del metodo
        if not self.current_method is None:
            for arg_id in functionCIL.params:
                if arg_id == _type.name:
                    return arg_id

        #cuando es un atributo global
        d = self.get_local()
        intr = AST_CIL.GetAttrib(d , 'self', self.class_attrs[self.current_class].index(_type.name))
        functionCIL.localvars.append(d)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(Plus)
    def visit(self, plus, functionCIL):
        #d = 'temp'

        d = self.get_local()

        #if not d in functionCIL.localvars:

        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Int')
        functionCIL.instructions.insert(0, intr1)

        a = self.visit(plus.first, functionCIL)
        b = self.visit(plus.second, functionCIL)
        intr = AST_CIL.Plus(d, a, b)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(Minus)
    def visit(self, minus, functionCIL):
        #d = 'temp'

        d = self.get_local()

        #if not d in functionCIL.localvars:

        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Int')
        functionCIL.instructions.insert(0, intr1)

        a = self.visit(minus.first, functionCIL)
        b = self.visit(minus.second, functionCIL)
        intr = AST_CIL.Minus(d, a, b)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(Div)
    def visit(self, div, functionCIL):
        #d = 'temp'

        d = self.get_local()

        # if not d in functionCIL.localvars:

        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Int')
        functionCIL.instructions.insert(0, intr1)

        a = self.visit(div.first, functionCIL)
        b = self.visit(div.second, functionCIL)
        intr = AST_CIL.Div(d, a, b)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(Star)
    def visit(self, star, functionCIL):
        #d = 'temp'

        d = self.get_local()

        # if not d in functionCIL.localvars:

        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Int')
        functionCIL.instructions.insert(0, intr1)

        a = self.visit(star.first, functionCIL)
        b = self.visit(star.second, functionCIL)

        intr = AST_CIL.Star(d, a, b)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(Assign)
    def visit(self, assign, functionCIL):
        result = self.visit(assign.expression, functionCIL)
        n = len(self.local_variables) - 1
        
        for i in range(n, -1, -1):
            local_id =  self.local_variables[i].id
            local_type = self.local_variables[i].type
            if local_id == assign.id:
                local = local_id + '_' + str(self.local_variables[i].line) + '_' + str(self.local_variables[i].index)
                intr = AST_CIL.Assign(local, local_type, result)
                functionCIL.instructions.append(intr)
                return local
        
        if not self.current_method is None:
                for arg_id, arg_type in self.info.classmethods[self.current_class][self.current_method][0]:
                    if arg_id == assign.id:
                        intr = AST_CIL.Assign(arg_id, arg_type, result)                        
                        functionCIL.instructions.append(intr)
                        return arg_id

        if assign.expression.static_type == 'Int':
            d = self.get_local()
            functionCIL.localvars.append(d)
            intr_1 = AST_CIL.Allocate(d, 'Int')
            intr_2 = AST_CIL.Assign(d, 'Int', result)
            intr = AST_CIL.SetAttrib('self' , self.class_attrs[self.current_class].index(assign.id), d)
            functionCIL.instructions.insert(0, intr_1)
            functionCIL.instructions.append(intr_2)       
            functionCIL.instructions.append(intr)
        else:
            intr = AST_CIL.SetAttrib('self' , self.class_attrs[self.current_class].index(assign.id), result)
            functionCIL.instructions.append(intr)

        return result

    @visitor.when(EqualThan)
    def visit(self, equalThan, functionCIL):
        d = self.get_local()
        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Bool')
        functionCIL.instructions.insert(0, intr1)
        a = self.visit(equalThan.first, functionCIL)
        b = self.visit(equalThan.second, functionCIL)

        if equalThan.first.static_type == 'String':
            intr=AST_CIL.EqualStrThanStr(d, a, b)
            functionCIL.instructions += [intr]
        else:
            intr = AST_CIL.EqualThan(d, a, b)
            functionCIL.instructions += [intr]
        return d

    @visitor.when(LowerThan)
    def visit(self, lower, functionCIL):
        d = self.get_local()
        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Bool')
        functionCIL.instructions.insert(0, intr1)
        a = self.visit(lower.first, functionCIL)
        b = self.visit(lower.second, functionCIL)        
        intr = AST_CIL.LowerThan(d, a, b)
        functionCIL.instructions += [intr]
        return d

    @visitor.when(LowerEqualThan)
    def visit(self, lowerEq, functionCIL):
        d = self.get_local()
        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Bool')
        functionCIL.instructions.insert(0, intr1)
        a = self.visit(lowerEq.first, functionCIL)
        b = self.visit(lowerEq.second, functionCIL)
        intr = AST_CIL.LowerEqualThan(d, a, b)
        functionCIL.instructions += [intr]
        return d

    @visitor.when(Not)
    def visit(self, neg, functionCIL):
        d = self.get_local()
        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Bool')
        functionCIL.instructions.insert(0, intr1)
        a = self.visit(neg.expr, functionCIL)
        intr = AST_CIL.Minus(d, self.const_1, a)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(IntegerComplement)
    def visit(self, integerComplement, functionCIL):
        d = self.get_local()
        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Int')
        functionCIL.instructions.insert(0, intr1)
        a = self.visit(integerComplement.expression, functionCIL)
        intr = AST_CIL.Minus(d, self.null_const, a)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(IsVoid)
    def visit(self, isVoid, functionCIL):
        d = self.get_local()
        functionCIL.localvars.append(d)
        intr1 = AST_CIL.Allocate(d, 'Bool')
        intr2 = AST_CIL.SetAttrib(d, 0, 0)
        functionCIL.instructions.insert(0, intr2)
        functionCIL.instructions.insert(0, intr1)
        a = self.visit(isVoid.expression, functionCIL)        
        return d

    @visitor.when(Loop)
    def visit(self, loop, functionCIL):

        start = 'START_' + self.get_label()
        do = 'DO_' + self.get_label()
        end = 'END_' + self.get_label()

        intr1 = AST_CIL.Label(start)
        functionCIL.instructions.append(intr1)
        w = self.visit(loop.while_expression, functionCIL)
        intr2 = AST_CIL.GotoIf(w, do)
        functionCIL.instructions.append(intr2)
        intr3 = AST_CIL.Goto(end)
        functionCIL.instructions.append(intr3)
        intr4 = AST_CIL.Label(do)
        functionCIL.instructions.append(intr4)
        l = self.visit(loop.loop_expression, functionCIL)
        intr5 = AST_CIL.Goto(start)
        functionCIL.instructions.append(intr5)
        intr6 = AST_CIL.Label(end)
        functionCIL.instructions.append(intr6)
        return l

    @visitor.when(Conditional)
    def visit(self, cond, functionCIL):
        then = self.get_label()
        fi = self.get_label()
        dest = self.get_local()
        functionCIL.localvars.append(dest)

        # intr = AST_CIL.Allocate(dest, cond.static_type)
        # functionCIL.instructions.insert(0, intr)

        if_expression = self.visit(cond.if_expression, functionCIL)
        functionCIL.instructions.append(AST_CIL.GotoIf(if_expression, then))
        result1 = self.visit(cond.else_expression, functionCIL)
        
        #change
        #functionCIL.instructions.append(AST_CIL.Assign(dest, cond.else_expression.static_type, result1))
        #functionCIL.instructions.append(AST_CIL.Assign(dest, cond.static_type, result1))
        functionCIL.instructions.append(AST_CIL.Copy(dest, result1))        
        functionCIL.instructions.append(AST_CIL.Goto(fi))
        functionCIL.instructions.append(AST_CIL.Label(then))
        result2 = self.visit(cond.then_expression, functionCIL)
        
        #change 
        #functionCIL.instructions.append(AST_CIL.Assign(dest, cond.then_expression.static_type, result2))
        #functionCIL.instructions.append(AST_CIL.Assign(dest, cond.static_type, result2))
        functionCIL.instructions.append(AST_CIL.Copy(dest, result2))
        functionCIL.instructions.append(AST_CIL.Label(fi))
        return dest

    # @visitor.when(LetVar)
    # def visit(self, let, functionCIL):
    #     for item in let.declarations:
    #         self.visit(item, functionCIL)
    #         self.local_variables.append(item)
        
    #     result = self.visit(let.in_expression, functionCIL)

    #     n = len(let.declarations)        
    #     m = len(self.local_variables)        
    #     for i in range(n): self.local_variables.pop(m - i - 1)
    #     return result

    @visitor.when(Case)
    def visit(self, case, functionCIL):
        current_type = self.get_local()
        parent = self.get_local()
        comparer = self.get_local()
        d = self.get_local()
        dest = self.get_local()
        functionCIL.localvars += [current_type, parent, comparer, d, dest]

        intr1 = AST_CIL.Allocate(comparer, 'Bool')
        intr2 = AST_CIL.Allocate(current_type, 'String')
        intr3 = AST_CIL.Allocate(parent, 'String')
        functionCIL.instructions.insert(0, intr1)
        functionCIL.instructions.insert(0, intr2)
        functionCIL.instructions.insert(0, intr3)

        expr_0 = self.visit(case.case_expression, functionCIL)

        name = 'Case_' + str(self.idCount)
        case_types = []
        for item in case.implications:
            case_types.append(item.var.type + '_class_name')
        intr4 = AST_CIL.Array(name, case_types)
        functionCIL.instructions.insert(0, intr4)

        intr5 = AST_CIL.GetParent(d, expr_0, name, len(case_types))
        intr6 = AST_CIL.SetAttrib(parent, 0, d)
        functionCIL.instructions.append(intr5)
        functionCIL.instructions.append(intr6)

        n = len(case.implications)
        labels = []
        for i in range(n): labels.append(self.get_label())
        label_end = self.get_label()

        for i in range(n):
            branch = case.implications[i]
            intr7 = AST_CIL.Load(current_type, branch.var.type + '_class_name')
            functionCIL.instructions.append(intr7)
            intr8 = AST_CIL.EqualStrThanStr(comparer, current_type, parent)
            functionCIL.instructions.append(intr8)
            intr9 = AST_CIL.GotoIf(comparer, labels[i])
            functionCIL.instructions.append(intr9)

        for i in range(n):
            branch = case.implications[i]
            functionCIL.instructions.append(AST_CIL.Label(labels[i]))

            self.local_variables.append(branch.var)
            instance =  branch.var.id + '_' + str(branch.var.line) + '_' + str(branch.var.index)
            functionCIL.localvars.append(instance)
            intr = AST_CIL.Copy(instance, expr_0)
            functionCIL.instructions.append(intr)
            
            result = self.visit(branch.expr, functionCIL)  

            m = len(self.local_variables)
            self.local_variables.pop(m - 1)
            
            functionCIL.instructions.append(AST_CIL.Copy(dest, result))          
            functionCIL.instructions.append(AST_CIL.Goto(label_end))        
        functionCIL.instructions.append(AST_CIL.Label(label_end))
        return dest

