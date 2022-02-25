import cmp.visitor as visitor 
from .ast_CIL import *

eol = '\n'
tab = '\t'

class CILCodegen:
    @visitor.on('node')
    def visit(self, node, frame):
        pass

    @visitor.when(CILProgramNode)
    def visit(self, node: CILProgramNode):
        code = '.TYPES\n\n'
        for t in node.types:
            code += self.visit(t)
        code += '\n'
        code += '.DATA\n\n'
        for d in node.data:
            code += self.visit(d) + '\n\n'
        code += '\n'
        code += '.CODE\n\n'
        for f in node.functions:
            code += self.visit(f) + '\n\n'
        return code

    @visitor.when(CILTypeNode)
    def visit(self, node: CILTypeNode):
        code = f'type {node.id} ' + '{\n'
        
        for c in node.attributes:
            code += self.visit(c)
        code += '\n'
       
        for m in node.methods:
            code += self.visit(m)
        code += '}\n'

        return code

    @visitor.when(CILDataNode)
    def visit(self, node: CILDataNode):
        code = f'{node.id.lex} = \"{text}\";'

    @visitor.when(CILFuncNode)
    def visit(self, node: CILFuncNode):
        code = f'function {node.id} ' + '{\n'
        for p in node.params:
            code += self.visit(p)
        code += eol
        for l in node.locals:
            code += self.visit(l)
        code += eol
        for i in node.instructions:
            try:
                code += self.visit(i)
            except:
                print(code)
                print('--------------------------')
                print(i)
        code += eol
        code += '}\n\n'
        return code

    @visitor.when(CILAttributeNode)
    def visit(self, node:  CILAttributeNode):
        return f'\tattribute {node.id};\n'

    @visitor.when(CILMethodNode)
    def visit(self, node: CILMethodNode):
        return f'\tmethod {node.id} : {node.function_id};\n'

    @visitor.when(CILParamNode)
    def visit(self, node: CILParamNode):
        return f'\tPARAM {node.id};\n'

    @visitor.when(CILLocalNode)
    def visit(self, node: CILLocalNode):
        return f'\tLOCAL {node.id};\n'

    @visitor.when(CILInstructionNode)
    def visit(self, node):
        pass
    
    @visitor.when(CILAssignNode)
    def visit(self, node: CILAssignNode):
        code = f'\t{node.id.lex} = ' 
        try:
            code += self.visit(node.expr)
        except:
            print(node.expr)
        code += ';\n'
        return code

    @visitor.when(CILSetAttributeNode)
    def visit(self, node: CILSetAttributeNode):
        return f'\tSETATTR {node.id.lex} {node.attr.lex} {node.var.lex};\n'

    @visitor.when(CILArgNode)
    def visit(self, node:CILArgNode):
        return f'\tARG {node.id};\n'

    @visitor.when(CILGotoNode)
    def visit(self, node: CILGotoNode):
        return f'\tGOTO {node.label.id};\n'

    @visitor.when(CILIfGotoNode)
    def visit(self, node:CILIfGotoNode):
        return f'\tIF {node.var.lex} GOTO {node.label.id};\n'

    @visitor.when(CILLabelNode)
    def visit(self, node: CILLabelNode):
        return f'{node.id}:\n'

    @visitor.when(CILReturnNode)
    def visit(self, node: CILReturnNode):
        return f'\tRETURN {node.var.lex};\n'

    @visitor.when(CILPrint)
    def visit(self, node: CILPrint):
        return f'\tPRINT {node.var.lex};\n'

    @visitor.when(CILExpressionNode)
    def visit(self, node: CILExpressionNode):
        pass

    @visitor.when(CILBinaryOperationNode)
    def visit(self, node: CILBinaryOperationNode):
        pass

    @visitor.when(CILGetAttribute)
    def visit(self, node: CILGetAttribute):
        return f'GETATTR {node.var.lex} {node.attr.lex}'

    @visitor.when(CILAllocateNode)
    def visit(self, node: CILAllocateNode):
        return f'ALLOCATE {node.type}'

    @visitor.when(CILTypeOfNode)
    def visit(self, node: CILTypeOfNode):
        return f'TYPEOF {node.var.lex}'

    @visitor.when(CILVCallNode)
    def visit(self, node: CILVCallNode):
        return f'VCALL {node.type} {node.func}'

    @visitor.when(CILLoadNode)
    def visit(self, node: CILLoadNode):
        return f'LOAD {node.var.lex}'

    @visitor.when(CILLengthNode)
    def visit(self, node: CILLengthNode):
        return f'LENGTH {node.var.lex}'

    @visitor.when(CILStringNode)
    def visit(self, node: CILStringNode):
        return f'STRING {node.var.id}'

    @visitor.when(CILReadNode)
    def visit(self, node: CILReadNode):
        return 'READ'

    @visitor.when(CILAtomicNode)
    def visit(self, node: CILAtomicNode):
        return f'{node.lex}'

    @visitor.when(CILNumberNode)
    def visit(self, node):
        return f'{node.lex}'
    @visitor.when(CILTypeConstantNode)
    def visit(self, node):
        return f'{node.lex}'
    @visitor.when(CILVariableNode)
    def visit(self, node):
        return f'{node.lex}'
    @visitor.when(CILStringNode)
    def visit(self, node):
        return f'{node.lex}'
    @visitor.when(CILPlusNode)
    def visit(self, node: CILPlusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} + {r}'

    @visitor.when(CILMinusNode)
    def visit(self, node: CILMinusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} - {r}'

    @visitor.when(CILStarNode)
    def visit(self, node: CILStarNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} * {r}'

    @visitor.when(CILDivNode)
    def visit(self, node: CILPlusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} / {r}'

    @visitor.when(CILLessNode)
    def visit(self, node: CILLessNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} < {r}'

    @visitor.when(CILElessNode)
    def visit(self, node: CILElessNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} <= {r}'
    
    @visitor.when(CILEqualsNode)
    def visit(self, node: CILEqualsNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f'{l} == {r}'
