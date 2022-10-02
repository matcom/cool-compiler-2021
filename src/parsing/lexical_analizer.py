import ply.lex as lex
import parsing.tokens_rules as tokens_rules
from cmp.utils import Token

def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.lex in {"{", "}", ";"}:
            if token.lex == "}":
                indent -= 1
            print("    " * indent + " ".join(str(t.token_type) for t in pending))
            pending.clear()
            if token.lex == "{":
                indent += 1
    print(" ".join([str(t.token_type) for t in pending]))

def find_column(input, lexpos):
    line_start = input.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1

def tokenize_cool_text(grammar, idx, type_id, string, num, data, errors, printing=False):
    # lexer starts with: lexpos = 0, lineno = 1, last_new_line = 0
    # lexpos: Within token rule functions, this points to the first character after the matched text.
    lexer = lex.lex(module = tokens_rules)
    lexer.last_new_line_pos = 0
    lexer.errors = errors 

    # Give the lexer some input
    lexer.input(data)

    lessequal = grammar.__getitem__("<=")
    rarrow = grammar.__getitem__("=>")
    larrow = grammar.__getitem__("<-")
    
    fixed_tokens_names = {
        t.Name: (t.Name, t)
        for t in grammar.terminals
        if t not in {idx, type_id, string, num, lessequal, rarrow, larrow}
    }

    fixed_tokens_names["larrow"] = ("<-", larrow)
    fixed_tokens_names["rarrow"] = ("=>", rarrow)
    fixed_tokens_names["lessequal"] = ("<=", lessequal)

    tokens = []
    pos_data = []
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: # append EOF
            if len(pos_data) > 0:
                last_lineno, last_col = pos_data[-1]
                col = last_col + len(tokens[-1].lex)
            else: # empty program
                last_lineno = 0
                col = -1
            tokens.append(Token("$", grammar.EOF, (last_lineno, find_column(data, col))))
            break  # No more input
        else:
            try:
                tval, ttype = fixed_tokens_names[tok.type]
            except:
                tval = tok.value
                if tok.type == "string":
                    ttype = string
                elif tok.type == "id":
                    ttype = idx
                elif tok.type == "type_id":
                    ttype = type_id
                else:
                    ttype = num
            tokens.append(Token(tval, ttype, (tok.lineno, find_column(data, tok.lexpos))))

    if printing:
        pprint_tokens(tokens)
    return tokens
