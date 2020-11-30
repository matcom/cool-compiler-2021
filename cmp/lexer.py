from cmp.utils import Token, tokenizer
from cmp.grammar import *

fixed_tokens = { t.Name: Token(t.Name, t) for t in G.terminals if t not in { idx, num, stringx, boolx }}

@tokenizer(G, fixed_tokens)
def tokenize_text(token):
    lex = token.lex
    try:
        float(lex)
        return token.transform_to(num)
    except ValueError:
        if lex[0] == '"' and lex[-1] == '"':
            return token.transform_to(stringx)
        if lex == 'true' or lex == 'false':
            return token.transform_to(boolx)
        return token.transform_to(idx)

def pprint_tokens(tokens, get=False):
    indent = 0
    pending = []
    result = ''
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            if get:
                result += '    '*indent + ' '.join(str(t.token_type) for t in pending) + '\n'
            else:
                print('    '*indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    if get:
        result += ' '.join([str(t.token_type) for t in pending]) + '\n'
        return result
    else:
        print(' '.join([str(t.token_type) for t in pending]))
