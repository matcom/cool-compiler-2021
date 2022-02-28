import sys
import lexer.lexer as lexer
import c_parser.parser as parser
from pipeline import Pipeline

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # input_file = "./tests/codegen/fib.cl"
        raise Exception("Incorrect number of arguments")
    
    program_file = open(input_file)
    program = program_file.read()
    program_file.close()

    pipe = Pipeline(program, lexer.CoolLexer(), parser.CoolParser())
    if pipe.errors:
        for error in pipe.errors:
            print(error)
        exit(1)
    else:
        out_file = input_file.split(".")
        out_file[-1] = "mips"
        out_file = ".".join(out_file)
        with open(out_file, 'w') as f:
            f.write(pipe.mipsCode)
            
if __name__ == "__main__":
    main()
