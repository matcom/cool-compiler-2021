import sys
import lexer.lexer as lexer
import c_parser.parser as parser
from pipeline import Pipeline

# with open('/home/yumenio/Documents/cmp/cool-compiler-2021/cool-compiler-2021/tests/semantic/self4.cl') as f:
# with open('./tests/codegen/hello_world.cl') as f:
#     program =  f.read()

# coolLexer = lexer.CoolLexer()
# coolLexer.build()
# tokens = coolLexer.input(program)
# # for error in coolLexer.errors:
# #     print(error)
# Pipeline(program, lexer.CoolLexer(),parser.CoolParser(), False)
# coolParser = parser.CoolParser()

# ast = coolParser.parse(lexer.CoolLexer(), program)
# for lexing_error in coolParser.lexer.errors:
#     print(lexing_error)
# for parsing_error in coolParser.errors:
#     print(parsing_error)
# a = 0

# if __name__ == '__main__':
#     # with open('examles/hello_world.cl', 'r') as fd:
#     with open(f'{sys.argv[1]}', 'r') as fd:
#         program = ''
#         temp = fd.read()
#         while temp:
#             program += temp
#             temp = fd.read()
#     coolLexer = lexer.CoolLexer()
#     coolLexer.build()
#     tokens = coolLexer.input(program)
#     # for error in coolLexer.errors:
#     #     print(error)
#     Pipeline(program, lexer.CoolLexer(),parser.CoolParser(), False)
#     coolParser = parser.CoolParser()
    
#     ast = coolParser.parse(lexer.CoolLexer(), program)
#     if len(coolParser.lexer.errors) == 0 and len(coolParser.errors) == 0:
#         exit(0)
#     else:
#         for lexing_error in coolParser.lexer.errors:
#             print(lexing_error)
#         for parsing_error in coolParser.errors:
#             print(parsing_error)
#         exit(1)
    
    # parser_object = parser.make_parser()
    # ast = parser_object.parse(inp)
    # semantic_object = check_semantic.CheckSemantic()
    # cil_object = cil.Cool2cil()
    # scope_root = semantic_object.visit(ast, None)
    # cil_object.visit(ast, scope_root)
    # mips_object = MIPS(cil_object)
    # mips_object.generate_mips()
    # inp = ''
    # with open('src/staticMipsCode.asm', 'r') as fd:
    #     temp = fd.read()
    #     while temp:
    #         inp += temp
    #         temp = fd.read()
    # with open(f'{argv[2]}', 'w') as fd:
    #     fd.write(inp)
    #     fd.write("\n")
    #     fd.write("# Start Mips Generated Code")
    #     fd.write("\n")
    #     for line in mips_object.mips_code:
    #         fd.write("\n" + line)


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]  # + " " + sys.argv[2] + " " + sys.argv[3]
    else:
        input_file = "../tests/semantic/eq2.cl"#"debbuging/tests/Auto/call1.cl"
    #   raise Exception("Incorrect number of arguments")

    program_file = open(input_file)
    program = program_file.read()
    program_file.close()
    
    # coolLexer = lexer.CoolLexer()
    # coolLexer.build()
    # tokens = coolLexer.input(program)
    # if coolLexer.errors:
    #     for error in coolLexer.errors:
    #         print(error.__str__())
    #     exit(1)

    pipe = Pipeline(program, lexer.CoolLexer(),parser.CoolParser(), False)
    if pipe.errors:
        for error in pipe.errors:
            print(error)
        exit(1)
    coolParser = parser.CoolParser()

    ast = coolParser.parse(lexer.CoolLexer(), program)
    if coolParser.lexer.errors:
        for lexing_error in coolParser.lexer.errors:
            print(lexing_error.__str__())
        exit(1)
    if coolParser.errors:
        for parsing_error in coolParser.errors:
            print(parsing_error)
        exit(1)
    # parser = Parser(Lexer())
    # ast = parser.parse(program)
    # if parser.errors:
    #     for error in parser.errors:
    #         print(error)
    #     exit(1)

    # run_pipeline(ast)


main()
