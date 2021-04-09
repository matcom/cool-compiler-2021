
import lexer.lexer as lexer
import c_parser.parser as parser

<<<<<<< HEAD
with open('/home/regnod/Documents/cmp_compiler 4to/cool-compiler-2021/tests/parser/assignment1.cl') as f:
=======
with open('/home/yumenio/Documents/cmp/cool-compiler-2021/cool-compiler-2021/tests/parser/operation4.cl') as f:
>>>>>>> 3ace997f0e9e89cdaebac0f589a9993ea441e2f7
    program =  f.read()

# coolLexer = lexer.CoolLexer()
# coolLexer.build()
# tokens = coolLexer.input(program)
# for error in coolLexer.errors:
#     print(error)
<<<<<<< HEAD
coolLexer = lexer.CoolLexer()
coolParser = parser.CoolParser()
ast = coolParser.parse(coolLexer, program)
=======
coolParser = parser.CoolParser()
ast = coolParser.parse(lexer.CoolLexer(), program)
for lexing_error in coolParser.lexer.errors:
    print(lexing_error)
for parsing_error in coolParser.errors:
    print(parsing_error)
>>>>>>> 3ace997f0e9e89cdaebac0f589a9993ea441e2f7
a = 0
