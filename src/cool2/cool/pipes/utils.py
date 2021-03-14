from cool.lexer.cool_lexer import ocur, ccur, semi

def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            print('    '*indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    print(' '.join([str(t.token_type) for t in pending]))

def print_errors(header:str, errors):
    print(f"=========== {header} ===============")
    print(*[f"- {error}\n" for error in errors])