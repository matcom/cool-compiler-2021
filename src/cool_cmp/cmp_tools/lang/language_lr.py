from cmp_tools.parser.parser_lr import LR0Parser,LR1Parser,SLR1Parser,LALR1Parser
from cmp_tools.grammar.grammar_parser import get_grammar_from_text
from cmp_tools.grammar.grammar_tokens import get_lexer_from_text
from cmp_tools.lang.language import Language 
        
def return_lr_parser(G,parser):
    parser = parser.lower()
    if parser == 'lr0':
        lr = LR0Parser(G)
    elif parser == 'lalr1':
        lr = LALR1Parser(G)
    elif parser == 'slr1':
        lr = SLR1Parser(G)
    elif parser == 'lr1':
        lr = LR1Parser(G)
    else:
        lr = None
    return lr

def build_LR(tok_def,gram_def,lr:str,errors):
    """
    gram_def: grammar definition or an instance of Grammar\n
    tok_def: tokens deefinition or an instance of Lexer\n
    lr: type of lr parser, can be ['lalr1', 'lr1', 'lr0', 'slr1']\n
    return a LanguageLR\n
    return None in case of errors
    """
    new_errors = []
    
    lex_gram = get_lexer_from_text(tok_def,new_errors) if isinstance(tok_def,str) else tok_def
    Gramm = get_grammar_from_text(gram_def,new_errors) if isinstance(gram_def,str) else gram_def
    
    for x in new_errors:
        errors.append(x)
    if lex_gram and Gramm:
        lr = return_lr_parser(Gramm,lr)
        if not lr:
            errors.append(f'{lr} is not a valid LR type of parser, try [lalr1, lr1, lr0, slr1]')
            return None
        if lr.errors:
            errors.extend(lr.errors)
            # return None
        return LanguageLR(Gramm,lex_gram,lr)
    return None

class LanguageLR(Language):

    def __init__(self, grammar, lexer, parser_lr,token_parse_dict={}):
        super().__init__(grammar,lexer,token_parse_dict)
        self.parser = parser_lr

    def get_derivation_tree(self,parse):
        return self.parser.get_derivation_tree(parse,False)
