from itertools import islice
from tools.utils import ContainerSet

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()
    else:
        for x in alpha:
            symbol_first = firsts[x]

            first_alpha.update(symbol_first)

            if not symbol_first.contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

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

        # P: x -> alpha
        for production in G.Productions:
            x = production.Left
            alpha = production.Right

            # get current First(x)
            first_x = firsts[x]

            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)

            # update First(x) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_x.hard_update(local_first)

    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def compute_follows(G, firsts):
    follows = {}
    change = True

    local_firsts = {}

    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        # P: X -> alpha
        for production in G.Productions:
            x = production.Left
            alpha = production.Right

            follow_x = follows[x]

            for i, Y in enumerate(alpha):

                if not Y.IsTerminal:

                    follow_y = follows[Y]

                    try:
                        first_beta = local_firsts[alpha, i]
                    except KeyError:
                        first_beta = local_firsts[alpha, i] = compute_local_first(firsts, islice(alpha, i + 1, None))

                    change |= follow_y.update(first_beta)

                    if i == len(alpha) - 1 or first_beta.contains_epsilon:
                        change |= follow_y.update(follow_x)

    # Follow(Vn)
    return follows
