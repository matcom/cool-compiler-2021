import sys

from gen_code import generate_code
from parser.parser import parser , errors_parsing
from lexer import lexer , errors_lexing
from semantic import semantic_check
from semantic.types import errors_semantic


def exit_with_error(error):
    print(f'CompilerError: {error}')
    exit(1)


def main():
    if len(sys.argv) != 2:
        exit_with_error("invalid number of arguments")

    input_data = ""
    input_file = sys.argv[1]
    try:
        with open(input_file) as f:
            input_data = f.read()
    except FileNotFoundError:
        exit_with_error(f'file {sys.argv[1]} not found')

    ast = parser.parse(input_data, lexer, tracking=True)
    if errors_lexing:
        for e in errors_lexing:
            print(e)
        exit(1)
    if errors_parsing:
        for e in errors_parsing:
            print(e)
        exit(1)

    semantic_check(ast)
    if errors_semantic:
        for e in errors_semantic:
            print(e)
        exit(1)

    cil_code = generate_code(ast)
    output_file = input_file[0:-2] + 'mips'

    with open(output_file, "w") as output:
        output.write(cil_code)


if __name__ == "__main__":
    main()
