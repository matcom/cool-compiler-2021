# import streamlit as st

from compiler.cmp.grammar import G

# from compiler.lexer.lexer import tokenize_text, pprint_tokens
from compiler.lexer.lex import CoolLexer
from sys import exit

from compiler.cmp.tools import LR1Parser
# from compiler.cmp.evaluation import evaluate_reverse_parse
# from compiler.visitors.formatter import FormatVisitor
# from compiler.visitors.type_collector import TypeCollector
# from compiler.visitors.type_builder import TypeBuilder
# from compiler.visitors.type_checker import TypeChecker
# from compiler.visitors.type_inferencer import TypeInferencer


def main(args):
    try:
        with open(args.file, "r") as fd:
            code = fd.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found")
        exit(1)

    lexer = CoolLexer()
    tokens, errors = lexer.tokenize(code)
    for error in errors:
        print(error)

    if errors:
        exit(1)
    
    parser = LR1Parser(G)
    parseResult, (failed, token) = parser(tokens, get_shift_reduce=True)
    if failed:
        print(f"{token.pos} - SyntacticError: ERROR at or near {token.lex}")
        exit(1)

    # print('\n'.join(repr(x) for x in parse))
    # print("---------------OPERATIONS---------------")
    # print(operations)
    # print('==================== AST ======================')
    # ast = evaluate_reverse_parse(parse, operations, tokens)
    # formatter = FormatVisitor()
    # tree = formatter.visit(ast)
    # print(tree)
    # print('============== COLLECTING TYPES ===============')
    # errors = []
    # collector = TypeCollector(errors)
    # collector.visit(ast)
    # context = collector.context
    # print('Errors:', errors)
    # print('Context:')
    # print(context)
    # print('=============== BUILDING TYPES ================')
    # builder = TypeBuilder(context, errors)
    # builder.visit(ast)
    # manager = builder.manager
    # print('Errors: [')
    # for error in errors:
    #     print('\t', error)
    # print(']')
    # print('Context:')import argparse
    # print('Errors: [')
    # for error in errors:
    #     print('\t', error)
    # print(']')
    # formatter = FormatVisitor()
    # tree = formatter.visit(ast)
    # print(tree)

    # return ast


text = """
class Main inherits IO {
    number: Int <- 5;

    main () : Object {
        testing_fibonacci(number)
    };

    testing_fibonacci(n: Int) : IO {{
        out_string("Iterative Fibonacci : ");
        out_int(iterative_fibonacci(5));
        out_string("\\n");

        out_string("Recursive Fibonacci : ");
        out_int(recursive_fibonacci(5));
        out_string("\\n");
    }};

    recursive_fibonacci (n: AUTO_TYPE) : AUTO_TYPE {
        if n <= 2 then 1 else recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2) fi
    };

    iterative_fibonacci(n: AUTO_TYPE) : AUTO_TYPE {
        let  i: Int <- 2, n1: Int <- 1, n2: Int <- 1, temp: Int in {
            while i < n loop
                let temp: Int <- n2 in {
                    n2 <- n2 + n1;
                    n1 <- temp;
                    i <- i + 1;
                }
            pool;
            n2;
        }
    };
};
"""

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CoolCompiler")
    parser.add_argument(
        "-f", "--file", type=str, default="code.cl", help="File to read cool code from"
    )

    args = parser.parse_args()

    main(args)
