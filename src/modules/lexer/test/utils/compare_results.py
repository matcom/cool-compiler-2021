from src.modules.lexer import CoolLexer
import os


def compare_results(tests_dir: str):
    tests = [(file) for file in os.listdir(tests_dir) if file.endswith(".cl")]

    for test in tests:
        fd = open(tests_dir + test)
        code = fd.read()
        lexer = CoolLexer(lexer_errors=[])
        for token in lexer.tokenize(code):
            print(token)
        fd2 = open(tests_dir + test[:-3] + "_error.txt")
        errors = fd2.read().split("\n")
        print("Lexer Errors: ", lexer.errors)
        print("Should Errors: ", errors)
        assert lexer.errors == errors
