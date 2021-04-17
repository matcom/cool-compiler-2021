from lib.lang.language_ll1 import build_LL1
from lib.lang.language_lr import build_LR
from lib.lang.language_regular import build_Lan_Reg
from lib.grammar.grammar_fixer import fix_common_prefix,fix_e_productions,fix_left_recursion,fix_useless_symbols
from lib.grammar.grammar_util import grammar_to_text
from lib.grammar.grammar_parser import get_grammar_from_text
from lib.utils.first_follow import compute_firsts, compute_follows

def build_LR_2(lr_type):
    def build(tok_def,gram_def,error):
        return build_LR(tok_def,gram_def,lr_type,error)
    return build