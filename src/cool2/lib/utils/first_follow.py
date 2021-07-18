from cmp.utils import ContainerSet

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    ###################################################
    # alpha == epsilon ? First(alpha) = { epsilon }
    ###################################################
    #                   <CODE_HERE>                   #
    if alpha_is_epsilon:
        first_alpha.set_epsilon()
        return first_alpha
    ###################################################
    ###################################################
    # alpha = X1 ... XN
    # First(X1) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
    ###################################################
    #                   <CODE_HERE>                   #
    change = False
    for i in alpha:
        if not firsts[i].contains_epsilon:
            # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
            change = True
        for j in firsts[i]:
            first_alpha.add(j)
        if change:
            break
    if not change:
        # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
        first_alpha.set_epsilon()    
    ###################################################
    # First(alpha)
    return first_alpha


def compute_firsts(G):
    
    firsts = {}
    change = True
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    while change:
        change = False
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            # get current First(X)
            first_X = firsts[X]
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def compute_follows(G,firsts):
    
    follows = { }
    change = True
    local_firsts = { }
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    while change:
        change = False
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            follow_X = follows[X]
            ###################################################
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            ###################################################
            #                   <CODE_HERE>                   #
            j = 0
            alpha2 = {}
            for i in alpha:
                alpha2[j] = i
                j+=1
            for i in alpha2.keys():
                y = alpha2[i]
                if y.IsNonTerminal:
                    local_firsts = compute_local_first(firsts,alpha[i+1:])
                    change |= follows[y].update(local_firsts)
                    if local_firsts.contains_epsilon:
                        change |= follows[y].update(follow_X)
            ###################################################
    # Follow(Vn)
    return follows