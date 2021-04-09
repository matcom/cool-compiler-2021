
import lexer.lexer as lexer
import c_parser.parser as parser

with open('/home/regnod/Documents/cmp_compiler 4to/cool-compiler-2021/tests/parser/assignment1.cl') as f:
    program =  f.read()

# coolLexer = lexer.CoolLexer()
# coolLexer.build()
# tokens = coolLexer.input(program)
# for error in coolLexer.errors:
#     print(error)
coolParser = parser.CoolParser()
ast = coolParser.parse(lexer.CoolLexer(), program)
for lexing_error in coolParser.lexer.errors:
    print(lexing_error)
for parsing_error in coolParser.errors:
    print(parsing_error)
a = 0
