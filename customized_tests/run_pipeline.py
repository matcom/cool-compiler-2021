# from src.cool_tokenizer import tokenize_cool_text
from src.lexical_analizer import tokenize_cool_text
from src.cool_grammar import define_cool_grammar
from src.cool_visitor import FormatVisitor

from src.shift_reduce_parsers import LR1Parser, DerivationTree
from src.errors import parsing_table_error, Error

from src.cmp.evaluation import evaluate_reverse_parse


def run_pipeline(text):
    # define grammar
    grammar, idx, typeIdx, string, num = define_cool_grammar()

    # tokenize text
    # tokens = tokenize_cool_text(grammar, text, idx, num, True)
    tokens = tokenize_cool_text(grammar, idx, typeIdx, typeIdx, string, num, text, [], True)

    # print(tokens)
    # try:
    parser = LR1Parser(grammar)
    parse, operations = parser([t.token_type for t in tokens])
    # print("\n".join(repr(x) for x in parse))
    # print(operations)

    ast = evaluate_reverse_parse(parse, operations, tokens)

    return ast
    # print(tree)
    #         derivation_list = parser(text)
