from code_generation import MyCodeGenerator
from lexer import MyLexer
from parser import MyParser
from semantic import MySemanticAnalyzer
import sys

if __name__ == "__main__":

    _mylexer = MyLexer()
    _myparser = MyParser()

    if len(sys.argv) > 1:
        _file = sys.argv[1]
        _cool_program = open(_file, encoding="utf-8").read()
        try:
            _mylexer_result = _mylexer.tokenize(_cool_program)
        except:
            pass
        
        if _mylexer.errors:
            print(_mylexer.errors[0])
            exit(1)
        try:
            myAst = _myparser.parse(_cool_program)
        except:
            pass

        if _myparser.errors:
            print(_myparser.errors[0])
            exit(1)

        # SemanticTODO
        semantic_analyzer = MySemanticAnalyzer(myAst)
        context, scope = semantic_analyzer.analyze()

        for e in semantic_analyzer.errors:
            print(e)
            exit(1)

        # CodeGenTODO
        code_generator = MyCodeGenerator(context=context)
        mips_code = code_generator.compile(myAst, scope)
        with open(f'{sys.argv[1][:-3]}.mips','w') as f:
            f.write(f'{mips_code}')
