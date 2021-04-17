from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal, SentenceFromIter)
from lib.utils.trie import TrieNode, Trie
from lib.utils.algorithms import permutation # FIX

# GRAMMAR FIXER UTILS
def change_grammar_from_productions(gramm:Grammar,new_productions):
    """
    Empty all non terminal and grammar productions\n
    and add all productions in new_productions to gramm
    """
    for x in gramm.nonTerminals:
        x.productions = []
    
    gramm.Productions = []
    
    for x in new_productions:
        gramm.Add_Production(x)
    
    return gramm

def generate_name(G:Grammar,idx,prefix = 'N'):
    new_key = prefix+'_'
    cur_idx = idx
    while f'{new_key}{cur_idx}' in G.symbDict.keys():
        cur_idx+=1
    return f'{new_key}{cur_idx}',cur_idx+1

def remove_unnecessary_symbols(gramm:Grammar,unnecesary):
    new_prod = []
    
    for prod in gramm.Productions:
        if not prod.Left in unnecesary:
            r_unne = [x for x in prod.Right if x in unnecesary]
            if not r_unne:
                new_prod.append(prod)
    
    for x in unnecesary:
        try:
            gramm.nonTerminals.remove(x)
        except ValueError:
            gramm.terminals.remove(x)
        gramm.symbDict.__delitem__(x.Name)

    change_grammar_from_productions(gramm,new_prod)

def build_reach(gramm:Grammar, symbol):
    """
    Return a set with the symbols that reach symbol
    """
    reach = set()
    reach.add(symbol)
    last_len = 0
    while last_len != len(reach):
        last_len = len(reach)
        for x in gramm.Productions:
            if any([y for y in x.Right if y in reach]):
                reach.add(x.Left)
    return reach
                
def fix_grammar(G,errors):
    """
    Check if G is LL1 and fix it if possible\n
    Removes the immediate left recursion and the common prefixes\n
    return the new grammar fixed if possible\n
    else return None
    """
    if not G:
        return None
    # Your code goes here
    new_errors = []
    
    G = fix_common_prefix(G)
    G = fix_left_recursion(G,new_errors)
    G = fix_unnecesary_prod(G)
    
    errors.extend(new_errors)
    if new_errors:
        return None
    return G


# LEFT RECURSION
# Esta implementado solamente la inmediata una sola vez Probar algo como E -> EE o algo por el estilo
def fix_left_recursion(grammar:Grammar, errors):
    '''
    Fix immediate left recursion of grammar\n
    return a fixed copy of grammar
    '''
    new_grammar = grammar.copy()
    new_grammar.Productions = []
    
    for n_ter in grammar.nonTerminals:
        for prod in n_ter.productions:
            if not prod.Right.IsEpsilon and prod.Right[0] == prod.Left:
                fix_non_terminal_left_recursion(n_ter,new_grammar, errors)
                break
        else:
            new_grammar.Productions.extend(n_ter.productions)
    
    return new_grammar

def fix_non_terminal_left_recursion(non_terminal:NonTerminal, grammar, errors):
    '''
    Fix immediate left recursion non_terminal in grammar\n
    '''
    new_name,idx = generate_name(grammar,0,non_terminal.Name)
    new_non_terminal = grammar.NonTerminal(new_name)
    
    left_prod = non_terminal.productions
    non_terminal.productions = []
    new_prod_new_n_ter = set()
    new_prod_old_n_ter = set()

    for prod in left_prod:
        if not prod.Right.IsEpsilon and prod.Right[0] == non_terminal:
            if len(prod.Right) > 1:
                sentence = [x for x in prod.Right[1:]]
                sentence.append(new_non_terminal)
                new_prod_new_n_ter.add(Production(new_non_terminal,SentenceFromIter(sentence)))
        else:
            sentence = [x for x in prod.Right]
            sentence.append(new_non_terminal)
            new_prod_new_n_ter.add(Production(new_non_terminal,grammar.Epsilon))
            new_prod_old_n_ter.add(Production(non_terminal,SentenceFromIter(sentence)))
    
    for prod in new_prod_new_n_ter:
        grammar.Add_Production(prod)
    
    if not new_prod_old_n_ter:
        errors.append(f'All productions of {non_terminal} begins with {non_terminal}, no string can be parsed by a left parse')
    
    for prod in new_prod_old_n_ter:
        grammar.Add_Production(prod)


# CLEANING GRAMMAR
def fix_unnecesary_prod(grammar:Grammar):
    grammar = fix_e_productions(grammar)
    grammar = fix_useless_symbols(grammar)
    return grammar


# COMMON PREFIX
def fix_common_prefix(grammar:Grammar):
    """
    returns a copy of grammar without common prefixes
    """
    G = grammar.copy()
    G.Productions = []
    
    for non_terminal in grammar.nonTerminals:
        trie = Trie()
        epsilon = False
        for x in non_terminal.productions:
            if not x.Right.IsEpsilon:
                trie.add(x.Right)
            else:
                epsilon = True
        non_terminal.productions = []
        if epsilon:
            G.Add_Production(Production(x.Left,G.Epsilon))
        for node in trie.top.sons:
            execute_node(trie.top.sons[node],non_terminal,[],G,0)
    return G
      
def execute_node(node:TrieNode,left,right:list,grammar:Grammar,idx):
    """
    Fills productions with the new grammar productions\n
    left: left part of the production\n
    right: right part of the production in a list\n
    productions: all the productions of the grammar without common prefixes\n
    idx: index of the generated name
    """
    right.append(node.value)
    if len(node.sons) > 1 or (len(node.sons) == 1 and node.terminal):
        name,idx = generate_name(grammar,idx,left.Name)
        new_prod = grammar.NonTerminal(name)
        right.append(new_prod)
        grammar.Add_Production(Production(left,SentenceFromIter(right)))
        left = new_prod
        if node.terminal:
            grammar.Add_Production(Production(left,grammar.Epsilon))
        for x in node.sons:
            right = []
            execute_node(node.sons[x],left,right,grammar,idx)
    elif len(node.sons) == 1:
        for key in node.sons:
            execute_node(node.sons[key],left,right,grammar,idx)
            break
    else:
        grammar.Add_Production(Production(left,SentenceFromIter(right)))


# e-PRODUCTIONS
def remove_e_productions(G):
    """
    returns a grammar with all epsilon productions eliminated\n
    and a set with the Non Terminal that reached epsilon productions\n
    return G,n_t_epsilon
    """

    n_t_epsilon = set()
    new_productions = []
    # Removes all epsilon transitions from the non terminals
    for x in G.Productions:
        if x.Right.IsEpsilon:
            n_t_epsilon.add(x.Left)
            x.Left.productions.remove(x)
        else:
            new_productions.append(x)
    
    change = 0
    while change != len(n_t_epsilon):
        change = len(n_t_epsilon)
        for prod in G.Productions:
            if len([x for x in prod.Right if x in n_t_epsilon]) == len(prod.Right): # All x in right is on n_t_epsilon
                n_t_epsilon.add(prod.Left)
    
    G.Productions = new_productions
    
    return G,n_t_epsilon

def add_new_productions(prod,new_productions,n_t_epsilon):
    """
    Add to new_productions the corresponding productions from\n
    permutate prod with the non_terminals in n_t_epsilon \n
    Ex: A->BCB,n_t_eps={B}\n
    add to new_productions {A->BCB, A->CB, A->BC, A->C}
    """
    had_epsilon = [False]*len(prod.Right)
    cant_epsilon = 0
    
    for i,x in enumerate(prod.Right):
        if x in n_t_epsilon:
            had_epsilon[i] = True
            cant_epsilon += 1
    
    for perm in permutation(cant_epsilon,2):
        new_prod_right = []
        perm_idx = 0
        for i,x in enumerate(had_epsilon):
            if not x:
                new_prod_right.append(prod.Right[i])
            elif perm[perm_idx]:
                new_prod_right.append(prod.Right[i])
            perm_idx = perm_idx+1 if x else perm_idx
        if new_prod_right:
            new_productions.add(Production(prod.Left,SentenceFromIter(new_prod_right)))
    if cant_epsilon == 0:
        new_productions.add(Production(prod.Left,prod.Right))
                    
def fix_e_productions(gramm:Grammar):
    """
    Returns a grammar without epsilon transitions.\n
    if gramm recognize epsilon then an augmented grammar\n
    is return with an epsilon transition on the start symbol
    """
    G = gramm
    
    G,n_t_epsilon = remove_e_productions(G)
    
    if G.startSymbol in n_t_epsilon:
        G = G.AugmentedGrammar(force=True)
        G.Add_Production(Production(G.startSymbol,G.Epsilon))
    else:
        G = G.copy()
    
    new_productions = set()
    
    for prod in gramm.Productions:
        add_new_productions(prod,new_productions,n_t_epsilon)
    
    for x in gramm.nonTerminals:
        x.productions = []
    
    for prod in new_productions:
        G.Add_Production(prod)
        
    return G


# NON DERIVE TERMINAL 
def update_derivation(production,derivation,left_derivation = True):
    symbol,sentence = production.Left,production.Right
    derive = []
    derive.append(production)
    if not symbol in derivation:
        if sentence.IsEpsilon:
            derive.extend(derivation[symbol.Grammar.Epsilon])
        elif not left_derivation:
            sentence = [ sentence[i] for i in range(len(sentence)-1,-1,-1) ] # sentence.reverse()
        for x in sentence:
            derive.extend(derivation[x])
        derivation[symbol] = derive

def fix_non_derive_terminal(gramm:Grammar,return_derivations = False,left_derivation = True):
    """
    Remove from gramm the non terminals A that dont satisfy:\n
    A->*w  where w in {G.T}*
    return grammar 
    return grammar,derivation
    """
    gramm = gramm.copy()
    
    derivation = { x:[Production(x,Sentence(x)),] for x in gramm.terminals }
    derivation[gramm.Epsilon] = [Production(gramm.Epsilon,Sentence(gramm.Epsilon)),]
    derive_something = set(gramm.terminals)
    productions = set(gramm.Productions)
    
    change = -1
    while change != len(derive_something):
        change = len(derive_something)
        to_remove = []
        for x in productions:
            if not any([y for y in x.Right if not y in derive_something]): # if y ->* w with w in T*
                derive_something.add(x.Left)
                update_derivation(x,derivation,left_derivation)
                to_remove.append(x)
        for x in to_remove: productions.remove(x)
    
    remove_unnecessary_symbols(gramm,[x for x in gramm.nonTerminals if x not in derive_something])
    
    if return_derivations:
        return gramm,derivation
    return gramm
         

# UNREACHABLE SYMBOLS
def fix_unreachable_symbols(gramm:Grammar):
    gramm = gramm.copy()
    
    pending = [gramm.startSymbol]
    reachable = set(pending)
    while pending:
        symb = pending.pop()
        for prod in symb.productions:
            for r in prod.Right:
                if not r in reachable:
                    reachable.add(r)
                    if isinstance(r,NonTerminal):
                        pending.append(r)
    
    remove_unnecessary_symbols(gramm,[x for x in gramm.nonTerminals + gramm.terminals if x not in reachable])
    
    return gramm  
                

# USELESS SYMBOLS
def fix_useless_symbols(gramm:Grammar):
    """
    fix the non derive on terminal,  non_terminals\n
    and the unreachable symbols from the start symbol 
    """
    gramm = fix_unit_productions(gramm)
    
    gramm = fix_non_derive_terminal(gramm)

    gramm = fix_unreachable_symbols(gramm)

    return gramm


# UNIT PRODUCTIONS
def get_unit_tuples(unit_productions):
    change = -1
    tuples = set([(x.Left,x.Right[0]) for x in unit_productions])
    while change != len(tuples):
        change = len(tuples)
        to_add = set()
        for t in tuples:
            for q in [x for x in tuples if t[1] == x[0]]:
                to_add.add((t[0],q[1]))
        tuples.update(to_add)
    return tuples
        

def fix_unit_productions(gramm:Grammar):
    """
    returns an equivalent grammar without productions of the form:\n
    A -> B
    """
    gramm = gramm.copy()
    
    unit_productions = {x for x in gramm.Productions if len(x.Right) == 1 and x.Right[0].IsNonTerminal}

    new_productions = set()
    
    for x in gramm.Productions:
        if not x in unit_productions:
            new_productions.add(x)
    
    pending = get_unit_tuples(unit_productions)
    
    while pending:
        l,r = pending.pop()
        for prod in r.productions:
            if not prod in unit_productions:
                new_productions.add(Production(l,prod.Right))
        
    return change_grammar_from_productions(gramm,new_productions)
