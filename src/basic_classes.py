import AST_CIL

class Build:
    def __init__(self, code, types):
        self.idCount = 0
        self.build_IO(code, types)
        self.build_Object(code, types)
        self.build_String(code, types)
        self.build_Int(code, types)
        self.build_Bool(code, types)

    def get_local(self):
        dest = 'local__' + str(self.idCount)
        self.idCount += 1
        return dest

    def build_Object(self, code, types):
        # abort() : Object
        # type_name() : String
        # copy() : SELF_TYPE
        pass

    def build_String(self, code, types):
        # length() : Int
        # concat(s : String) : String
        # substr(i : Int, l : Int) : String
        pass

    def build_Int(self, code, types):
        pass

    def build_Bool(self, code, types):
        pass

    def build_IO(self, code, types):
        _type_IO = AST_CIL.Type('IO')
        func = 'function' + '_' + 'IO' + '_' + 'out_string'
        _type_IO.methods['out_string'] = func
        f = AST_CIL.Function(func)
        f.params.append('x')
        f.instructions.append(AST_CIL.PrintStr('x'))
        f.instructions.append(AST_CIL.Return('self'))
        code.append(f)
        ################################################
        func = 'function' + '_' + 'IO' + '_' + 'out_int'
        _type_IO.methods['out_int'] = func
        f = AST_CIL.Function(func)
        f.params.append('x')
        f.instructions.append(AST_CIL.PrintInt('x'))
        f.instructions.append(AST_CIL.Return('self'))
        code.append(f)
        ################################################
        func = 'function' + '_' + 'IO' + '_' + 'in_int'
        _type_IO.methods['in_int'] = func
        f = AST_CIL.Function(func)
        d = self.get_local()
        f.localvars.append(d)
        f.instructions.append(AST_CIL.ReadInt(d))
        instance = self.get_local()
        intr1 = AST_CIL.Allocate(instance, 'Int')
        intr2 = AST_CIL.SetAttrib(instance, 0, d)
        f.localvars.append(instance)
        f.instructions += [intr1, intr2]
        f.instructions.append(AST_CIL.Return(instance))        
        code.append(f)
        types.append(_type_IO)
