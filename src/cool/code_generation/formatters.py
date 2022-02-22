import cool.code_generation.ast_cil as cil
import cool.code_generation.ast_mips as mips
import cool.visitor as visitor


class CilFormatter:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        dottypes = "\n".join(self.visit(t) for t in node.dottypes)
        dotdata = "\n".join(self.visit(t) for t in node.dotdata)
        dotcode = "\n".join(self.visit(t) for t in node.dotcode)

        return f".TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}"

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        parent = f"inherits from {node.parent}"
        attributes = "\n\t".join(f"attribute {x}" for x in node.attributes)
        methods = "\n\t".join(f"method {x}: {y}" for x, y in node.methods)

        r = f"type {node.name} {{\n\t{parent}"
        if attributes:
            r += f"\n\n\t{attributes}"
        if methods:
            r += f"\n\n\t{methods}"
        r += "\n}"
        return r

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        params = "\n\t".join(self.visit(x) for x in node.params)
        local_vars = "\n\t".join(self.visit(x) for x in node.local_vars)
        instructions = "\n\t".join(self.visit(x) for x in node.instructions)

        s = f"function {node.name}{{\n\t{params}"
        if local_vars:
            s += f"\n\n\t{local_vars}"
        if instructions:
            if len(node.instructions) >= 2:
                s += f"\n\n\t{instructions}"
            else:
                s += f"\n\t{instructions}"
        s += "\n}"

        return s

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        return (
            f"PARAM {node.name}"
            if node.comment == ""
            else f"PARAM {node.name} # {node.comment}"
        )

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        return (
            f"LOCAL {node.name}"
            if node.comment == ""
            else f"LOCAL {node.name} # {node.comment}"
        )

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        return (
            f"{node.dest} = {node.source}"
            if node.comment == ""
            else f"{node.dest} = {node.source} # {node.comment}"
        )

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        return (
            f"{node.dest} = {node.left} + {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} + {node.right} # {node.comment}"
        )

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        return (
            f"{node.dest} = {node.left} - {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} - {node.right} # {node.comment}"
        )

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        return (
            f"{node.dest} = {node.left} * {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} * {node.right} # {node.comment}"
        )

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        return (
            f"{node.dest} = {node.left} / {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} / {node.right} # {node.comment}"
        )

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        return (
            f"{node.dest} = {node.left} == {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} == {node.right} # {node.comment}"
        )

    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        return (
            f"{node.dest} = {node.left} < {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} < {node.right} # {node.comment}"
        )

    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        return (
            f"{node.dest} = {node.left} <= {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} <= {node.right} # {node.comment}"
        )

    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        return (
            f"{node.dest} = XOR {node.left} {node.right}"
            if node.comment == ""
            else f"{node.dest} = XOR {node.left} {node.right} # {node.comment}"
        )

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        return (
            f"{node.dest} = ALLOCATE {node.type}"
            if node.comment == ""
            else f"{node.dest} = ALLOCATE {node.type} # {node.comment}"
        )

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        return (
            f"{node.dest} = TYPEOF {node.obj}"
            if node.comment == ""
            else f"{node.dest} = TYPEOF {node.obj} # {node.comment}"
        )

    @visitor.when(cil.TypeDirectionNode)
    def visit(self, node: cil.TypeDirectionNode):
        return (
            f"{node.dest} = TYPEDIR {node.name}"
            if node.comment == ""
            else f"{node.dest} = TYPEDIR {node.name} # {node.comment}"
        )

    @visitor.when(cil.AncestorNode)
    def visit(self, node: cil.AncestorNode):
        return (
            f"{node.dest} = ANCESTOR {node.obj}"
            if node.comment == ""
            else f"{node.dest} = ANCESTOR {node.obj} # {node.comment}"
        )

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        return (
            f"{node.dest} = CALL {node.function}"
            if node.comment == ""
            else f"{node.dest} = CALL {node.function} # {node.comment}"
        )

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        return (
            f"{node.dest} = VCALL {node.type} {node.method}"
            if node.comment == ""
            else f"{node.dest} = VCALL {node.type} {node.method} # {node.comment}"
        )

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        return (
            f"{node.dest} = GETATTR {node.instance} {node.attr}"
            if node.comment == ""
            else f"{node.dest} = GETATTR {node.instance} {node.attr} # {node.comment}"
        )

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        return (
            f"SETATTR {node.instance} {node.attr} {node.source}"
            if node.comment == ""
            else f"SETATTR {node.instance} {node.attr} {node.source} # {node.comment}"
        )

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        return (
            f"ARG {node.name}"
            if node.comment == ""
            else f"ARG {node.name} # {node.comment}"
        )

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        return (
            f"\n\tRETURN {node.value if node.value is not None else 0}"
            if node.comment == ""
            else f"\n\tRETURN {node.value if node.value is not None else 0} # {node.comment}"
        )

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        return (
            f"GOTO {node.address}"
            if node.comment == ""
            else f"GOTO {node.address} # {node.comment}"
        )

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoNode):
        return (
            f"IF {node.condition} GOTO {node.address}"
            if node.comment == ""
            else f"IF {node.condition} GOTO {node.address} # {node.comment}"
        )

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        return (
            f"{node.label}:"
            if node.comment == ""
            else f"{node.label}: # {node.comment}"
        )

    @visitor.when(cil.ArrayNode)
    def visit(self, node: cil.ArrayNode):
        return (
            f"{node.dest} = ARRAY {node.size}"
            if node.comment == ""
            else f"{node.dest} = ARRAY {node.size} # {node.comment}"
        )

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        return (
            f"{node.dest} = GETINDEX {node.instance} {node.index}"
            if node.comment == ""
            else f"{node.dest} = GETINDEX {node.instance} {node.index} # {node.comment}"
        )

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        return (
            f"SETINDEX {node.instance} {node.index} {node.source}"
            if node.comment == ""
            else f"SETINDEX {node.instance} {node.index} {node.source} # {node.comment}"
        )

    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode):
        return "HALT" if node.comment == "" else f"HALT # {node.comment}"

    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        return (
            f"{node.dest} = TYPENAME {node.source}"
            if node.comment == ""
            else f"{node.dest} = TYPENAME {node.source} # {node.comment}"
        )

    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode):
        return (
            f"{node.dest} = COPY {node.source}"
            if node.comment == ""
            else f"{node.dest} = COPY {node.source} # {node.comment}"
        )

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        return (
            f"PRINTSTR {node.str_addr}"
            if node.comment == ""
            else f"PRINTSTR {node.str_addr} # {node.comment}"
        )

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        return (
            f"PRINTINT {node.value}"
            if node.comment == ""
            else f"PRININT {node.value} # {node.comment}"
        )

    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        return (
            f"READSTR {node.dest}"
            if node.comment == ""
            else f"PRININT {node.dest} # {node.comment}"
        )

    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        return (
            f"READINT {node.dest}"
            if node.comment == ""
            else f"READINT {node.dest} # {node.comment}"
        )

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        return (
            f"{node.dest} = LENGTH {node.str_address}"
            if node.comment == ""
            else f"{node.dest} = LENGTH {node.str_address} # {node.comment}"
        )

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        return (
            f"{node.dest} = CONCAT {node.str1} {node.str2}"
            if node.comment == ""
            else f"{node.dest} = CONCAT {node.str1} {node.str2} # {node.comment}"
        )

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        return (
            f"{node.dest} = SUBSTRING {node.str_address} {node.start} {node.length}"
            if node.comment == ""
            else f"{node.dest} = SUBSTRING {node.str_address} {node.start} {node.length} # {node.comment}"
        )

    @visitor.when(cil.CommentNode)
    def visit(self, node: cil.CommentNode):
        return f"# {node.comment}"

    @visitor.when(cil.EmptyInstruction)
    def visit(self, node: cil.EmptyInstruction):
        return "" if node.comment == "" else f"# {node.comment}"


class MipsFormatter:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        dotdata = "\n\t".join([self.visit(data) for data in node.dotdata])
        dottext = "\n\t".join([self.visit(data) for data in node.dottext])

        return f".data\n\t{dotdata}\n\n.text\n\t{dottext}"

    @visitor.when(mips.DataNode)
    def visit(self, node: mips.DataNode):
        return f"{node.name}: {node.data_type} {node.value}"

    @visitor.when(mips.OneAddressInstructionNode)
    def visit(self, node: mips.OneAddressInstructionNode):
        return f"{node.code} {node.dest}"

    @visitor.when(mips.TwoAddressIntructionNode)
    def visit(self, node: mips.TwoAddressIntructionNode):
        return f"{node.code} {node.dest} {node.source}"

    @visitor.when(mips.ThreeAddressIntructionNode)
    def visit(self, node: mips.ThreeAddressIntructionNode):
        return f"{node.code} {node.dest}, {node.source1}, {node.source2}"

    @visitor.when(mips.LabelNode)
    def visit(self, node: mips.LabelNode):
        return f"{node.name}:"

    @visitor.when(mips.EmptyDataNode)
    def visit(self, node: mips.EmptyDataNode):
        return ""
