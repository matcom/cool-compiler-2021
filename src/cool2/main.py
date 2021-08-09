import os, sys
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(base_dir, ".."))

from cool.pipeline import cool_pipeline, reconstr_pipeline
from cool.grammar.cool_grammar import G
from cool.parser.cool_parser import save_parser,cool_parser_path, cool_parser
from cool.lexer.cool_lexer import save_lexer,cool_lexer_path, cool_tokens_def
from cool.grammar.comment_grammar import C
from cool.parser.comment_parser import comment_parser_path, comment_parser
from cool.lexer.comment_lexer import comment_lexer_path, comment_tokens_def
import plac

# plac annotation (description, type of arg [option, flag, positional], abrev, type, choices)
def main(
    program_dir:("Path to cool program", "positional"),
    output_dir:("Path for the compiled mips", "positional"),
    out_infer:("Creates a file containing the inferred types", 'flag', 'i'),
    verbose:("Print more info", 'flag', 'v'),
    update_cool_parser:("Update pickled cool parser", 'flag', 'ucp'),
    update_cool_lexer:("Update pickled cool lexer", 'flag', 'ucl'),
    update_comment_parser:("Update pickled comment parser", 'flag', 'ump'), 
    update_comment_lexer:("Update pickled comment lexer", 'flag', 'uml')):
    """
    Manage cool interpreter and run programs
    """
    change = False
    if update_cool_parser:
        obj = save_parser(cool_parser_path,G)
        print('Errors',obj.errors)
        print("Parser updated")
        change |= True

    if update_cool_lexer:
        obj = save_lexer(cool_tokens_def,cool_lexer_path,G)
        print("Lexer updated")
        change |= True

    if update_comment_parser:
        obj = save_parser(comment_parser_path,C)
        print('Errors',obj.errors)
        print("Comment Parser updated")
        change |= True

    if update_comment_lexer:
        obj = save_lexer(comment_tokens_def,comment_lexer_path,C)
        print("Comment Lexer updated")
        change |= True

    if change:
        print("Parsers and Lexers updated")
        exit()

    if program_dir == None:
        print("If no update flag is provided 'program_dir' is required")
        exit(1)
    
    with open(program_dir) as file:
        file_content = file.read()
    
    if out_infer:
        result = reconstr_pipeline(file_content, verbose=verbose)
    else:
        result = cool_pipeline(file_content,verbose=verbose)
    ast, g_errors, parse, tokens, context, scope, operator, value, reconstr = [result.get(x, None) for x in ["ast", "errors", "text_parse", "text_tokens", "context", "scope", "operator", "value", "reconstructed_text"]] 
    
    if reconstr and out_infer:
        with open(program_dir + ".infer.cl", "w") as file:
            file.write(reconstr)
    
    if g_errors:
        for err in g_errors:
            print(err)
        exit(1)
    # if hasattr(value, "value"):
    #     print("Value:",value.value)    
    
if __name__ == "__main__":
    plac.call(main)