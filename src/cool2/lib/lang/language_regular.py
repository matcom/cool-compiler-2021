from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceFromIter, SentenceList, Symbol,
                            Terminal)
from cmp.utils import ContainerSet, Token, inspect, pprint
from lib.grammar.grammar_parser import get_grammar_from_text
from lib.grammar.grammar_tokens import get_lexer_dict_from_text,get_lexer_from_text
from lib.lang.language_lr import LanguageLR,return_lr_parser
from lib.lexer.lexer import cap_letters, digits, min_letters
from lib.lexer.regex import EPSILON, regex_automaton
from lib.utils.automaton import *

def copy_automaton(base_automaton):
    """
    Returns a tuple of base_automaton properties\n
    start, states, finals, transitions
    """
    start = base_automaton.start
    dif = base_automaton.states
    finals = base_automaton.finals.copy()

    transitions = {}
    for x in base_automaton.transitions:
        for y in base_automaton.transitions[x]:
            transitions[x,y] = base_automaton.transitions[x][y]

    return start,dif,finals,transitions

def join(raw_automaton,raw_automaton_join,state1,state2):
    """
    raw_automaton, raw_automaton_join: tuples of copy_automatons\n
    state1, state2: states of raw_automaton\n
    insert raw_automaton_join in raw_automaton between state1 and state2\n
     ______                                                                           ______
    (state1)--[symb in transitions[start of join automaton]]-->raw_automaton_join--e-->(state2)
    """
    start, dif, finals, transitions = raw_automaton
    j_start, j_dif, j_finals, j_transitions = raw_automaton_join

    for symb in [s for x,s in j_transitions if x == j_start]:
        try:
            transitions[state1,symb].append(j_transitions[j_start,symb][0] + dif)
        except KeyError:
            transitions[state1,symb] = [j_transitions[j_start,symb][0] + dif]

    for f in j_finals:
        transitions[f+dif,''] = [state2]

    for state,symb in j_transitions:
        transitions[state + dif,symb] = [j_transitions[state,symb][0] + dif]

    return start,dif+j_dif,finals,transitions

def join_automaton(base_automaton,lex_dic): ################ convertir los States de lex_dic en DFA
    """
    base_automaton: automaton from grammar, (deterministic)
    lex_dic: dictionary that maps the terminals to the automaton that recognize it
    """

    start, dif, finals, transitions = copy_automaton(base_automaton)
    fixed_transitions = transitions.copy()
    transitions = {}
    raw = start, dif, finals, transitions
    cached_automaton = {}

    for state,terminal in fixed_transitions:
        try:
            au = cur_start, cur_states, cur_finals, cur_transitions = cached_automaton[terminal]
        except KeyError:
            automaton = lex_dic[terminal]
            au = cur_start, cur_states, cur_finals, cur_transitions = copy_automaton(automaton)
            cached_automaton[terminal] = au

        raw = join(raw,au,state,fixed_transitions[state,terminal][0])

    nfa = NFA(raw[1],raw[2],raw[3],raw[0])
    dfa = nfa_to_dfa(nfa)
    mini = automata_minimization(dfa)

    return mini

def build_automaton_from_grammar(tok_def,gram_def,errors,lexer=None,grammar=None):
    """
    Return the NFA if the grammar is regular
    else return None
    """
    new_errors = []

    lex = get_lexer_from_text(tok_def,errors) if not lexer else lexer
    G = get_grammar_from_text(gram_def,errors) if not grammar else grammar

    if G == None or lex == None:
        errors.append('Invalid grammar or token definition')
        return None

    if not check_grammar_regular(G, errors):
        errors.append('Invalid Regular Grammar')
        return None

    symb_num = {}
    transitions = {}
    itr1 = iter(range(len(G.nonTerminals)))
    for x in G.nonTerminals:
        symb_num[x] = next(itr1)

    start = symb_num[G.startSymbol]
    finals = [len(G.nonTerminals)]

    distinguish_on_epsilon = any([x for x in G.startSymbol.productions if x.IsEpsilon])
    if distinguish_on_epsilon: finals.append(start)

    for prod in G.Productions:
        left = symb_num[prod.Left]
        len_right = len(prod.Right)
        first_symbol = prod.Right[0]
        if len_right == 2:
            try:
                transitions[left,first_symbol.Name].add(symb_num[prod.Right[1]])
            except KeyError:
                transitions[left,first_symbol.Name] = {symb_num[prod.Right[1]]}
        elif len_right == 1:
            try:
                transitions[left,first_symbol.Name].add(finals[0])
            except KeyError:
                transitions[left,first_symbol.Name] = {finals[0]}

    nfa = NFA(len(G.nonTerminals)+1,finals,transitions,start)
    dfa = nfa_to_dfa(nfa)
    mini = automata_minimization(dfa)

    return mini # join_automaton(mini,lex.regexs) ##############################################

def check_grammar_regular(G:Grammar,errors):
    """
    return True if the Grammar G is regular
    """
    new_errors = []
    for prod in G.Productions:
        left = prod.Left
        right = prod.Right
        if right.IsEpsilon :
            if left != G.startSymbol:
                new_errors.append(f'Invalid Production for Regular Grammar: {prod}; the only left part that can have an epsilon on right part is the distiguish state')
            continue
        if len(right) > 2:
            new_errors.append(f'Invalid Production for Regular Grammar: {prod}; the lenght of right part must be at most 2 and is {len(right)}')
        else:
            if not right[0].IsTerminal:
                new_errors.append(f'Invalid Production for Regular Grammar: {prod}; the first symbol on a right part must be a terminal')
            if len(right) == 2:
                if right[1].IsTerminal:
                    new_errors.append(f'Invalid Production for Regular Grammar: {prod}; the second symbol on a right part must be a non terminal')
    errors.extend(new_errors)
    return not bool(new_errors)

# REGULAR GRAMMAR TO REGEX

def eliminate_state(tupled_automaton,s):
    start,states,finals,transitions = tupled_automaton
    
    assert s != start,"you cant eliminate the start state"

    start = start if start < s else start - 1
    try:
        finals.remove(s)
    except:
        pass
    finals = { x for x in map(lambda x: x if x < s else x-1,finals)} 
    
    exit_s = []  
    enter_s = []
    other = []
    new_transitions = {}
    cycle = ''
    
    for x in transitions.items(): # cycles in s dont go anywhere just 'activate' cycle variable
        (state,value),regex = x
        if state == s:
            if value == s:
                cycle = f'({regex})*'
                continue
            exit_s.append(x)
        elif value == s:
            enter_s.append(x)
        else:
            other.append(x)
    
    for (state0, value0),regex0 in enter_s:
        for (state1, value1),regex1 in exit_s:
            third = first(lambda x: x[0][0] == state0 and x[0][1] == value1,other)
            if third:
                other.remove(third)
            transition = f"{third[1]}|" if third else ""
            state = state0 if state0 < s else state0 - 1
            value = value1 if value1 < s else value1 - 1
            new_transitions[state,value] = f"({transition}{regex0}{cycle}{regex1})"
    
    for (state0, value0),regex0 in other:
        state0 = state0 if state0 < s else state0 - 1
        value0 = value0 if value0 < s else value0 - 1
        if [x for (state,value), regex in new_transitions.items() if state == state0 and value == value0]:
           print("WTF!!") 
        new_transitions[state0,value0] = regex0
    
    return start,states-1,finals,new_transitions

def eliminate_all_non_start_non_finals(tupled_automaton):
    """
    return a tuple of start,states,finals,transitions of the automaton from eliminate all the \n
    non start and the non finals states
    """
    start,states,finals,transitions = tupled_automaton
    change = True
    while change:
        change = False
        for s in range(states):    
            if not s in finals and s != start:
                change = True
                tupled_automaton = start,states,finals,transitions = eliminate_state(tupled_automaton,s)   
                break
    return tupled_automaton

def eliminate_all_non_start_non_t(tupled_automaton,t):
    """
    return a tuple of start,states,finals,transitions of the automaton from eliminate all the \n
    non start and the non t states
    """
    start,states,finals,transitions = tupled_automaton
    change = True
    while change:
        change = False
        for s in range(states):    
            if s != t and s != start:
                change = True
                tupled_automaton = start,states,finals,transitions = eliminate_state(tupled_automaton,s)   
                t = t if s > t else t-1
                break
    return tupled_automaton

def get_key(start,end,transitions):
    # key = first(lambda x: x[0][0] == start and x[1] == end,transitions.items())
    try:
        key = transitions[start,end]
    except KeyError:
        key = ''
    return key#[0][1] if key else ''

def get_regex_from_reduced_automaton(tupled_automaton):
    """
    tupled_automaton: an automaton with de form:\n
    (A)--regex->(A)<-regex_left  regex_right->(B)<-regex--(B)\n
    or\n
    (AB)--regex->(AB)\n
    where A is start and B is final\n 
    """
    start,states,finals,transitions = tupled_automaton
    if states == 2:
        other = 0 if start == 1 else 1
        A = get_key(start,start,transitions)
        B = get_key(start,other,transitions)
        C = get_key(other,other,transitions)
        D = get_key(other,start,transitions)
        if not B:
            return ''
        if A and C and D:
            return f"({A}|{B}{C}*{D})*{B}{C}*"
        if A and D:
            return f"({A}|{B}{D})*{B}"
        if A and C:
            return f"{A}*{B}{C}*"
        if A:
            return f"{A}*{B}"
        if C and D:
            return f"({B}{C}*{D})*{B}{C}*"
        if C:
            return f"{B}{C}*"
        if D:
            return f"({B}{D})*{B}"
        return f"{B}"
    if states == 1:
        assert start in finals, "start is not a final state"
        A = get_key(start,start,transitions)
        if A:
            return f"{A}*"
        else:
            return ''
    assert False, "Wrong number of states in the tupled automaton"
            
def regex_from_clean_automaton(tupled_automaton,s):
    """
    tupled_automaton: an automaton with only finals states and the start state
    s: final state to find regex
    return the regex from eliminate all the states except the start state and the s state
    """
    tupled_automaton = eliminate_all_non_start_non_t(tupled_automaton,s)
    
    return get_regex_from_reduced_automaton(tupled_automaton)
            
def convert_to_regex_automaton(tupled_automaton):
    """
    join al the transitions from state x to state y in one equivalent regex\n
    example:\n
    (A)-a,b,c->(B)  => (A)-a|b|c->(B)
    """
    start,states,finals,transitions = tupled_automaton

    temp_dic = {}
    for (state,symbol),values in transitions.items():
        for value in values:
            try:
                regex = temp_dic[state,value]
                regex = regex[:len(regex)-1] + f"|{symbol})"
            except KeyError:
                regex = f'({symbol})'
            temp_dic[state,value] = regex
    
    transitions = temp_dic
                
    return start,states,finals,transitions

def build_regex_from_grammar(tok_def,gram_def,errors:list,lexer=None,grammar=None,automaton=None):
    """
    return the regex and the automaton from tok_def and gram_def or from lexer and grammar if automaton is not given\n
    else return the regex of the automaton given
    """
    new_errors = []
    
    if not automaton:
        automaton = build_automaton_from_grammar(tok_def,gram_def,new_errors,lexer,grammar)
        if not automaton:
            errors.extend(new_errors)
            return None

    tupled_automaton = copy_automaton(automaton)
    tupled_automaton = convert_to_regex_automaton(tupled_automaton)
    tupled_automaton = start,states,finals,transitions = eliminate_all_non_start_non_finals(tupled_automaton)
    iter_finals = finals.copy()
    regex = []
    for s in iter_finals:
        new_transitions = transitions.copy()
        new_finals = finals.copy()
        automaton = start,states,new_finals,new_transitions
        new_regex = regex_from_clean_automaton(automaton,s)
        regex.append(new_regex)
    
    if new_errors:
        errors.extend(new_errors)

    regex = '|'.join(regex)
    
    tupl = regex_automaton(regex,return_regex=True)
    return tupl[1]



def build_Lan_Reg(tok_def,gram_def,errors):
    """
    gram_def: grammar definition or an instance of Grammar\n
    tok_def: tokens deefinition or an instance of Lexer\n
    return a LanguageRegular\n
    return None in case of errors
    """
    lexer = get_lexer_from_text(tok_def,errors) if isinstance(tok_def,str) else tok_def
    grammar = get_grammar_from_text(gram_def,errors) if isinstance(gram_def,str) else gram_def

    if not grammar or not lexer:
        errors.append('Invalid grammar or token definition')
        return None

    if not check_grammar_regular(grammar,errors):
        errors.append('Invalid Regular Grammar')
        return None

    return LanguageRegular(grammar,lexer)

class LanguageRegular(LanguageLR):

    grammar_regex = None

    grammar_automaton = None

    def __init__(self, grammar, lexer):
        super().__init__(grammar,lexer,None)

    def grammar_to_regex(self,errors):
        self.grammar_regex = self.grammar_regex if self.grammar_regex else build_regex_from_grammar('','',errors,self.lexer,self.grammar,self.grammar_to_automaton(errors))
        return self.grammar_regex

    def grammar_to_automaton(self,errors):
        self.grammar_automaton = self.grammar_automaton if self.grammar_automaton else build_automaton_from_grammar('','',errors,self.lexer,self.grammar)
        return self.grammar_automaton

    def __call__(self, string,errors):
        automaton = self.grammar_to_automaton(errors)
        if automaton:
            return automaton.recognize(string),None
        return None,None

