from utils.semantic import Scope, Context
from visitors.Depicter import Depicter
from visitors.Collector import TypeCollector
from visitors.Builder import TypeBuilder
from visitors.Checker import TypeChecker
from visitors.CooltoCil import COOLToCILVisitor
from visitors.CiltoMips import CILToMipsVisitor


class Pipeline():
    def __init__(self, program, lexer, parser, verbose=False):
        self.context: Context = Context()
        self.scope: Scope = Scope()
        self.program = program
        self.parser = parser
        self.lexer = lexer
        self.ast = self.parser.parse(self.lexer, self.program)
        self.errors = self.lexer.errors + self.parser.errors
        
        if len(self.errors) != 0:
            return
        
        if self.ast is None:
            return
                
        self.depicter = Depicter()
        if verbose:
            print(self.depicter.visit(self.ast, 0), '\n')
            print()
        
        self.typeCollector = TypeCollector(self.context, self.errors)
        self.typeCollector.visit(self.ast)
        if len(self.errors) == 0:
            self.typeBuilder = TypeBuilder(self.context, self.errors)
            self.typeBuilder.visit(self.ast)
            scope = Scope()
            if len(self.errors) == 0:
                self.typeChecker = TypeChecker(self.context, self.errors)
                self.typeChecker.visit( self.ast, scope)
                if len(self.errors) == 0:
                    self.coolToCil = COOLToCILVisitor(self.context)
                    cil_ast = self.coolToCil.visit(self.ast, scope)
                    
                    self.cilToMips = CILToMipsVisitor()
                    self.mipsCode = self.cilToMips.visit(cil_ast)
        return
