from src.cmp.utils import Token, tokenizer


def tokenize_cool_text(G, text, idx, num, print_tokens=False):
    fixed_tokens = {
        t.Name: Token(t.Name, t) for t in G.terminals if t not in {idx, num}
    }

    @tokenizer(G, fixed_tokens)
    def tokenize_text(token):
        lex = token.lex
        try:
            float(lex)
            return token.transform_to(num)
        except ValueError:  # verificar los string
            return token.transform_to(idx)

    # (do something like if(lex[0] == " and lex[-1] =="))
    tokens = tokenize_text(text)
    if print_tokens:
        pprint_tokens(tokens)
    return tokens


# pie co los lex, arreglar como toca
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


# if __name__ == "__main__":
#     pprint_tokens(tokens)

