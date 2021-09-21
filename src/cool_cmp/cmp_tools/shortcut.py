from cmp_tools.lang.language_ll1 import build_LL1
from cmp_tools.lang.language_lr import build_LR
from cmp_tools.lang.language_regular import build_Lan_Reg
from cmp_tools.grammar.grammar_fixer import fix_common_prefix,fix_e_productions,fix_left_recursion,fix_useless_symbols
from cmp_tools.grammar.grammar_util import grammar_to_text
from cmp_tools.grammar.grammar_parser import get_grammar_from_text
from cmp_tools.utils.first_follow import compute_firsts, compute_follows

def build_LR_2(lr_type):
    def build(tok_def,gram_def,error):
        return build_LR(tok_def,gram_def,lr_type,error)
    return build