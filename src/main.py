
import lexer.lexer as lexer
import c_parser.parser as parser

with open('/home/yumenio/Documents/cmp/cool-compiler-2021/cool-compiler-2021/tests/lexer/comment1.cl') as f:
    program =  f.read()

coolLexer = lexer.CoolLexer()
coolLexer.build()
tokens = coolLexer.input(program)
# coolParser = parser.CoolParser()
# ast = coolParser.parse(coolLexer, program)
a = 0
