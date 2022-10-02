from cmp.pycompiler import Item
from cmp.automata import State, lr0_formatter, multiline_formatter
from cmp.utils import ContainerSet
from parsing.methods import compute_firsts, compute_local_first, compute_follows

# LR0 automaton -> for SLR and LALR parsers
def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, "Grammar must be augmented"

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [start_item]
    visited = {start_item: automaton}

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        # (Decide which transitions to add)
        # agregar las epsilon transiciones
        # a estados donde el item posee producciones a partir del simbolo actual en la posicion 0
        # y agregar la transicion a partir del simbolo siguiente

        next_item = current_item.NextItem()
        try:
            next_state = visited[next_item]
        except KeyError:
            next_state = State(next_item, True)
            visited[next_item] = next_state
            pending.append(next_item)

        if current_item.NextSymbol.IsNonTerminal:
            epsilon_productions = current_item.NextSymbol.productions
        else:
            epsilon_productions = None

        current_state = visited[current_item]
        # (Adding the decided transitions)
        current_state.add_transition(current_item.NextSymbol.Name, next_state)

        if epsilon_productions:
            for eproduction in epsilon_productions:
                epItem = Item(eproduction, 0)
                try:
                    epState = visited[epItem]
                except KeyError:
                    epState = State(epItem, True)
                    visited[epItem] = epState
                    pending.append(epItem)
                current_state.add_epsilon_transition(epState)

    return automaton


# LR1 automaton
def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    # (Compute lookahead for child items)
    previews = item.Preview()
    for preview in previews:
        lookaheads.update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    # (Build and return child items)
    items = []
    for production in next_symbol.productions:
        items.append(Item(production, 0, lookaheads))

    return items


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {
        Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()
    }


def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        # Your code here!!!
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert (
        just_kernel or firsts is not None
    ), "`firsts` must be provided if `just_kernel=False`"
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, "Grammar must be augmented"

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])  # como cabecera solo queda el kernel

    closure = closure_lr1(start, firsts)
    automaton = State(
        frozenset(closure), True
    )  # en visited si se guarda el estado completo

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        closure = closure_lr1(current, firsts)
        for symbol in G.terminals + G.nonTerminals:
            # (Get/Build `next_state`)
            # closure = closure_lr1(current,firsts)
            goto = goto_lr1(closure, symbol, firsts, True)

            if not goto:
                continue

            try:
                next_state = visited[goto]
            except KeyError:
                next_state = visited[goto] = State(
                    frozenset(closure_lr1(goto, firsts)), True
                )
                pending.append(goto)

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton


def build_LALR_automaton(G):
    assert len(G.startSymbol.productions) == 1, "Grammar must be augmented"

    lr1_automaton = build_LR1_automaton(G)

    same_kernel = {}
    for node in lr1_automaton:
        just_center = frozenset([item.Center() for item in node.state])
        try:
            same_kernel[just_center].append(node)
        except KeyError:
            same_kernel[just_center] = [node]

    start = frozenset(
        [item.Center() for item in lr1_automaton.state]
    )  # como cabecera solo quedan los items sin lookahead
    automaton = State(
        lr1_automaton.state, True
    )  # en visited se guarda el estado que corresponde a la fusion de estaods ocn el mismo nucleo

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]  # se van a actualizar
        # todos los estados con los que el estado actual tiene alguna transicion
        lr1_state = same_kernel[current][0]

        # chequear que cada estado del cjto analizado tenga esa transicion
        for symbol in G.terminals + G.nonTerminals:
            if lr1_state.has_transition(symbol.Name):
                state = lr1_state.transitions[symbol.Name][0]
                center_items = frozenset([item.Center() for item in state.state])
                try:
                    next_state = visited[center_items]
                except KeyError:
                    kernel_set = same_kernel[center_items]
                    items_with_lookahead = {}
                    for node in kernel_set:
                        for item in node.state:
                            try:
                                current_item = items_with_lookahead[item.Center()]
                            except KeyError:
                                current_item = items_with_lookahead[
                                    item.Center()
                                ] = set()
                            current_item.update(item.lookaheads)
                    completed_items = [
                        Item(item.production, item.pos, lookaheads)
                        for item, lookaheads in items_with_lookahead.items()
                    ]
                    next_state = State(frozenset(completed_items), True)
                    visited[center_items] = next_state
                    pending.append(center_items)

                current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton
