from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal, SentenceFromIter)
from cmp.utils import ContainerSet, inspect, pprint, Token
from lib.grammar.grammar_tokens import get_lexer_from_text
from lib.grammar.grammar_parser import get_grammar_from_text
from lib.lexer.lexer import digits,min_letters,cap_letters
from lib.parser.parser_ll1 import ParserLL1
from lib.grammar.grammar_fixer import fix_grammar
from lib.lang.language import Language
class LanguageLL1(Language):

    def __init__(self, grammar,lexer):
        super().__init__(grammar,lexer)
        self.parser = ParserLL1(self.grammar)

    @property
    def get_firsts(self):
        return self.parser.get_firsts
    
    @property
    def get_follows(self):
        return self.parser.get_follows
    
    @property
    def get_predictive_table(self):
        return self.parser.get_parser_table
    
    def get_derivation_tree(self,parse):
        return self.parser.get_derivation_tree(parse)
        
def build_LL1(tokens_def, grammar_def, errors:list):
    """
    token_def:\n
    The definition of the non terminal symbols of the grammar\n
    (the name must be equal to the non terminals written in grammar_def)\n
    token_def --> same format than text in get_lexer function\n 
    token_def can be an instance of Lexer in case of already have it\n
    grammar_def:\n
    The definition by the user of the grammar in this format:\n
    Production1;Production2;...ProductionN;\n
    A production can be: T ~ A bc |r3 | epsilon\n
    grammar_def can be an instance of Grammar in case of already have it\n
    return None if the grammar is not LL1\n
    return the LanguageLL1 defined in grammar_def \n
    """
    new_errors = []
    lex_gram = get_lexer_from_text(tokens_def,new_errors) if isinstance(tokens_def,str) else tokens_def
    Gramm = get_grammar_from_text(grammar_def,new_errors) if isinstance(grammar_def,str) else grammar_def
    # Gramm = fix_grammar(Gramm,errors)

    if not Gramm or not lex_gram:
        for x in new_errors:
            errors.append(x)
        return None
    ll1 = LanguageLL1(Gramm,lex_gram)
    for x in ll1.parser.errors:
        new_errors.append(x)
    for x in new_errors:
        errors.append(x)
    # if new_errors:
    #     return None
    return ll1 
