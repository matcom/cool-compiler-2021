from cmp.pycompiler import (
    Symbol,
    NonTerminal,
    Terminal,
    EOF,
    Sentence,
    SentenceList,
    Epsilon,
    Production,
    Grammar,
)
from cmp.utils import ContainerSet
from errors import parsing_table_error, invalid_sentence_error
from itertools import islice
from cmp.automata import State


# Computes First(alpha), given First(Vt) and First(Vn)
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    ###################################################
    # alpha == epsilon ? First(alpha) = { epsilon }
    ###################################################
    if alpha_is_epsilon or len(alpha) == 0:
        first_alpha.set_epsilon()
        return first_alpha
    ###################################################

    ###################################################
    # alpha = X1 ... XN
    # First(Xi) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
    ###################################################
    if alpha[0].IsTerminal:
        first_alpha.add(alpha[0])
        return first_alpha

    #     if alpha[0].IsNonTerminal:
    #         first_alpha.update(firsts[alpha[0]])

    for item in alpha:
        if firsts[item].contains_epsilon:
            first_alpha.update(firsts[item])
        else:
            first_alpha.update(firsts[item])
            break

    else:
        first_alpha.set_epsilon()

    ###################################################

    # First(alpha)
    return first_alpha


# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
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
            except:
                first_alpha = firsts[alpha] = ContainerSet()

            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)

            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    # First(Vt) + First(Vt) + First(RightSides)
    return firsts


def compute_follows(G, firsts):
    follows = {}
    change = True

    # local_firsts = {}

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

            for i in range(0, len(alpha) - 1):
                if alpha[i].IsNonTerminal:
                    beta = Sentence(*alpha[i + 1 :])
                    firsts_beta = compute_local_first(firsts, beta)
                    change |= follows[alpha[i]].update(firsts_beta)

                    if firsts_beta.contains_epsilon:
                        change |= follows[alpha[i]].update(follow_X)

            if not alpha.IsEpsilon and alpha[-1].IsNonTerminal:
                change |= follows[alpha[-1]].update(follow_X)

            ###################################################

    # Follow(Vn)
    return follows

