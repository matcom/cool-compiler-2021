from cmp.utils import Token

class Language():

    parser = None

    grammar = None

    lexer = None

    def __init__(self, grammar,lexer,token_parse_dict={}):
        self.grammar = grammar
        self.lexer = lexer
        self.token_parse = token_parse_dict

    def _fix_tokens(self,tokens,errors):
        """
        If there are a token_type named 'space' this are discarted from the parsing tokens\n
        also transform lexer tokens to grammar tokens 
        """
        fix_tokens = []
        for x in tokens:
            if x.token_type != 'space':
                try:
                    if x.token_type in self.token_parse:
                        tok = Token(self.token_parse[x.token_type](x.lex),x.token_type)
                    else:
                        tok = Token(x.lex,x.token_type)
                    fix_tokens.append(tok)
                except KeyError:
                    errors.append(f'The grammar does not recognize the token {x}')
        return fix_tokens

    def __call__(self, text, errors, tokens=None):
        """
        returns a tuple of the parse and the tokens of the text
        """

        if tokens is None:
            tokens = self.get_tokens(text, errors)

        parse_errors = []
        parse = self.parser(tokens,parse_errors)

        for x in parse_errors:
            errors.append(x)

        if parse_errors:
            return [],[]
        
        return parse,tokens
    
    def get_tokens(self, text, errors):
        """
        Return the text tokens
        """
        tokens = self.lexer(text)
        # tokens = self._fix_tokens(tokens,errors)
        # for tok in tokens:
        #     tok.lex = (tok.lex[0], tok.lex[1] + 1, tok.lex[2] - len(tok.lex[0]) + 1) 
        #     if tok.token_type == "UNKNOWN":
        #         errors.append(f'({tok.lex[1]}, {tok.lex[2]}) - LexicographicError: ERROR "{tok.lex[0]}"')
        # tokens = [x for x in tokens if x.token_type != "UNKNOWN"]
        
        return tokens
        
    def find_conflict(self):
        return self.parser.find_conflict()
    
    def evaluate(self, text, errors:list,return_ast = False):
        # tokens = [ x for x in self.lexer(text) if x.token_type != 'space']
        tokens = self._fix_tokens(self.lexer(text),errors)
        return self.parser.evaluate(tokens,errors,return_ast)
