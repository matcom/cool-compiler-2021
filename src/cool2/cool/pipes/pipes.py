
from cool.lexer.cool_lexer import cool_lexer
from cool2.cool.lexer.ply_cool_lexer import PlyLexer
from cool.lexer.comment_lexer import comment_lexer
from lib.lang.language_lr import LanguageLR
from cool.parser.cool_parser import cool_parser
from cool.parser.comment_parser import comment_parser
from cool.visitors.visitors import *
from cool.grammar.cool_grammar import G, comment_open, comment_close
from cool.grammar.comment_grammar import C
from cool.semantic.scope import Scope
from cool.pipes.utils import pprint_tokens, print_errors
from cool.pipes.pipeline import Pipe

ply_lexer = PlyLexer()

def start_pipe(text, verbose = False):
    """
    Start the pipeline  
    """
    result = {
        "text": text,
        "verbose": verbose,
        "errors": [],
    }
    return result

start_pipe = Pipe(start_pipe)

def change_escaped_lines(result:dict, escape_regex="\\\ *?\n"):
    import re
    text, _ = re.subn(escape_regex, "", result['text'])
    result["text"] = text
    return result

change_escaped_lines = Pipe(change_escaped_lines)

def remove_comments_pipe(result:dict, comment_grammar=C, comment_lexer=comment_lexer, comment_parser=comment_parser):
    """
    Remove the commented lines from the text
    """
    text = result["text"]
    
    lang = LanguageLR(comment_grammar, comment_lexer, comment_parser)
    errors = []
    parse, tokens = lang(text, errors)
    if not errors:
        text = comment_parser.evaluate(tokens, errors, True)
    
    if result.get("verbose",False):
        if errors:
            print_errors("Removing Comments Errors", errors)
        if len(text) != len(result["text"]):
            print("=========== Text Comments Removed ===============")
            print(text)
        else:
            print("=========== No Comments Removed ===============")
    
    result["errors"].extend(errors)
    result["text"] = text

    return result

remove_comments_pipe = Pipe(remove_comments_pipe)

def remove_comment_tokens_pipe(result:dict):
    """
    Remove all tokens between (* *) and their respective errors if any
    """
    tokens = result["text_tokens"]
    errors = result["errors"]
    new_tokens = []
    new_errors = []
    deep = 0
    start_comment_position, end_comment_position = None, None
    for tok in tokens:
        if tok.token_type == comment_open:
            deep+=1
            start_comment_position = (tok.lex[1], tok.lex[2])
        elif tok.token_type == comment_close:
            deep-=1
            if deep == 0:
                end_comment_position = (tok.lex[1], tok.lex[2])
                # Removing errors related to comments
                errors = [x for x in errors if not (start_comment_position <= (x.row, x.column) <= end_comment_position)]
        elif not deep:
            new_tokens.append(tok)
            
    if result.get("verbose",False):
        if errors:
            print_errors("Nested Comment Elimination Errors", errors)
    
    result["errors"] = errors
    result["errors"].extend(new_errors)
    
    result.update({
        "text_tokens": new_tokens
    })
    return result

remove_comment_tokens_pipe = Pipe(remove_comment_tokens_pipe)

def tokenize_text_pipe(result:dict, language_grammar=G, language_lexer=cool_lexer, language_parser=cool_parser):
    """
    Tokenize the text
    """
    text = result['text']
    
    lang = LanguageLR(language_grammar, language_lexer, language_parser)
    
    errors = []
    tokens = lang.get_tokens(text, errors)
    
    result.update({
        "parser": language_parser,
        "lexer": language_lexer,
        "language": lang,
        "text_tokens": tokens,
    })

    if result.get("verbose",False):
        if errors:
            print_errors("Lexer Errors", errors)
        print('================== TOKENS =====================')
        pprint_tokens(tokens)
    
    result["errors"].extend(errors)

    return result

tokenize_text_pipe = Pipe(tokenize_text_pipe)

def ply_lexer_pipe(result:dict, language_grammar=G, language_lexer=ply_lexer, language_parser=cool_parser):
    """
    Tokenize with ply
    """
    text = result["text"]

    lang = LanguageLR(language_grammar, language_lexer, language_parser)

    errors = []
    tokens = lang.get_tokens(text, errors)

    errors = language_lexer.get_errors()

    result.update({
        "parser"        : language_parser,
        "lexer"         : language_lexer,
        "language"      : lang,
        "text_tokens"   : tokens
    })

    if result.get("verbose", False):
        if errors:
            print_errors("Lexer Errors", errors)

        print('================== TOKENS =====================')
        pprint_tokens(tokens)

    result["errors"].extend(errors)

    return result

ply_lexer_pipe = Pipe(ply_lexer_pipe)

def parse_text_pipe(result:dict, language_grammar=G, language_lexer=PlyLexer(), language_parser=cool_parser):
    """
    Parse the text
    """
    text = result['text']
    tokens = result.get('text_tokens')
    
    lang = result.get('language', LanguageLR(language_grammar, language_lexer, language_parser))
    
    errors = []
    parse, tokens = lang(text, errors, tokens)
    
    
    if result.get("verbose",False):
        if errors:
            print_errors("Parsing Text Errors", errors)
        if not 'text_tokens' in result:
            print('================== TOKENS =====================')
            pprint_tokens(tokens)
        print('=================== PARSE =====================')
        print('\n'.join(repr(x) for x in parse))
    
    result.update({
        "text_parse": parse,
        "language": lang,
        "text_tokens": tokens,
        "parser":language_parser
    })
    
    result["errors"].extend(errors)

    return result

parse_text_pipe = Pipe(parse_text_pipe)

def ast_pipe(result:dict):
    """
    Add the initial ast
    """
    parser = result["parser"]
    tokens = result["text_tokens"]
    text_parsed = result.get("text_parse", None)
    
    errors = []
    if text_parsed or tokens:
        ast = parser.evaluate(tokens,errors,True,text_parsed)
        result["ast"] = ast
        
    if result.get("verbose", False):
        if errors:
            print_errors("Building AST Errors", errors)
        print('==================== AST ======================')
        formatter = FormatVisitor()
        tree = formatter.visit(ast)
        print(tree)

    result["errors"].extend(errors)
    
    return result

ast_pipe = Pipe(ast_pipe, lambda x: not x["errors"])
    
def type_collector_pipe(result:dict, collector=TypeCollector):
    """
    Collects the types in the program.
    """
    ast = result.get("ast", None)
    if not ast:
        return result
    
    errors = []
    collector = collector(errors, result.get("context", None))
    collector.visit(ast)
    context = collector.context
    
    result["context"] = context
    
    if result.get("verbose", False):
        if errors:
            print_errors("Collecting Types Errors", errors)
        print('============== COLLECTED TYPES ===============')
        print(context)
        
    result["errors"].extend(errors)
    
    return result

type_collector_pipe = Pipe(type_collector_pipe)

def build_types_pipe(result:dict, builder=TypeBuilder):
    """
    Build the types in context
    """
    ast = result.get("ast", None)
    context = result.get("context",None)
    if not ast or not context:
        return result
    
    errors = []
    builder = builder(context, errors)
    builder.visit(ast)
    
    if result.get("verbose", False):
        if errors:
            print_errors("Building Types Errors", errors)
        print('=============== BUILT TYPES ================')
        print(context)
        
    result["errors"].extend(errors)
    
    return result

build_types_pipe = Pipe(build_types_pipe)

def check_types_pipe(result:dict, checker=TypeChecker):
    """
    Build the scope and check for types to be ok
    """
    
    ast = result.get("ast", None)
    context = result.get("context",None)
    if not ast or not context:
        return result
            
    errors = []
    checker = checker(context, errors)
    scope, operator = checker.visit(ast, Scope())

    result["scope"] = scope
    result["operator"] = operator
    
    if result.get("verbose", False):
        if errors:
            print_errors("Checking Types Errors", errors)
        print("=========== Checked Types Info =============")
        print("Scope:")
        print(scope)
        print("Operator:")
        print(operator)
    
    result["errors"].extend(errors)
    
    return result    

check_types_pipe = Pipe(check_types_pipe)

def run_program_pipe(result:dict, runner=RunVisitor):
    """
    Run ast and store the result
    """
    ast = result.get("ast",None)
    context = result.get("context",None)
    scope = result.get("scope",None)
    operator = result.get("operator",None)
    errors = result.get("errors", None)
    if any(x == None for x in [ast, context, scope, operator]) or errors:
        return result
    
    errors = []
    runner = runner(context,scope,operator,errors)
    value = runner.visit(ast)
    
    result["value"] = value
    
    if result.get("verbose", False):
        if errors:
            print_errors("Running Program Errors", errors)
        print('=============== PROGRAM RAN ===============')
        print('Returned Value:')
        print(value)
    
    result["errors"].extend(errors)
    
    return result

run_program_pipe = Pipe(run_program_pipe, lambda x: not x["errors"])

def reconstruct_pipe(result:dict, reconstructer=ReconstructVisitor):
    ast = result.get("ast",None)
    context = result.get("context",None)
    operation = result.get("operator",None)
    if any(x == None for x in [ast, context, operation]):
        return result
    
    reconstructer = reconstructer(context, operation)
    reconstructed_text = reconstructer.visit(ast)
    if result.get("verbose", False):
        print("============== Reconstructed Text ===============")
        print(reconstructed_text)
    result['reconstructed_text'] = reconstructed_text
    return result

reconstruct_pipe = Pipe(reconstruct_pipe)

def void_as_type_pipe(result:dict):
    
    tokens = result.get("text_tokens",None)
    if not tokens:
        return result
    
    result["errors"].extend([f"Void cant appear explicitly. Line:{x.lex[1]} Column:{x.lex[2]}" for x in tokens if x.token_type.Name == "type" and x.lex[0] == "Void"])
    return result

void_as_type_pipe = Pipe(void_as_type_pipe)

def auto_resolver_pipe(result:dict, auto_resolver=AutoResolver):
    ast = result.get("ast",None)
    context = result.get("context",None)
    if any(x == None for x in [ast, context]):
        return result
    
    errors = []
    resolver = auto_resolver(context, errors)
    resolver.visit(ast)
    
    if result.get("verbose", False):
        if errors:
            print_errors("Auto Resolver Errors", errors)
    
    result["errors"].extend(errors)
    
    return result

auto_resolver_pipe = Pipe(auto_resolver_pipe)

def string_escape_pipe(result:dict):
    tokens = result["text_tokens"]
    import re
    for tok_str in [x for x in tokens if x.token_type.Name == "string"]:
        text = re.sub(r"\\n","\n",tok_str.lex[0])
        text = re.sub(r"\\b","\b",text)
        text = re.sub(r"\\t","\t",text)
        text = re.sub(r"\\f","\f",text)
        tok_str.lex = (text, tok_str.lex[1], tok_str.lex[2])
    return result
    
string_escape_pipe = Pipe(string_escape_pipe)