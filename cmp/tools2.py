from cmp.utils import *
from cmp.nfa_dfa import *
from cmp.automata import *
from cmp.pycompiler import *
from itertools import islice
import cmp.visitor as visitor

class Node:
    def evaluate(self):
        raise NotImplementedError()

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return NFA(1, [0], {})

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(2, [1], {(0, s) : [1],})

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)


#this method is used for updating ll1 table as well as action-goto table
def upd_table(table, head, symbol, production):
    if not head in table:
        table[head] = {}
    if not symbol in table[head]:
        table[head][symbol] = []
    if production not in table[head][symbol]:
        table[head][symbol].append(production)
    return (len(table[head][symbol]) <= 1)


def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

    return first_alpha

def compute_firsts(G):
    firsts = {}
    change = True

    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False

        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            first_X = firsts[X]

            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    return firsts

def compute_follows(G, firsts):
    follows = { }
    change = True

    local_firsts = {}

    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            follow_X = follows[X]

            for i, Y in enumerate(alpha):
                if Y.IsNonTerminal:
                    try:
                        beta_f = local_firsts[alpha, i]
                    except KeyError:
                        beta_f = local_firsts[alpha, i] = compute_local_first(firsts, islice(alpha, i + 1, None))
                    change |= follows[Y].update(beta_f)
                    if beta_f.contains_epsilon:
                        change |= follows[Y].update(follow_X)

    return follows

def build_parsing_table(G, firsts, follows):
    M = {}
    ok = True

    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        for t in firsts[alpha]:
            ok &= upd_table(M, X, t, production)

        if firsts[alpha].contains_epsilon:
            for t in follows[X]:
                ok &= upd_table(M, X, t, production)

    return M, ok

def deprecated_metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):

    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M, _ = build_parsing_table(G, firsts, follows)

    def parser(w):

        stack =  [G.EOF, G.startSymbol]
        cursor = 0
        output = []

        while True:
            top = stack.pop()
            a = w[cursor]

            if top.IsEpsilon:
                pass
            elif top.IsTerminal:
                assert top == a
                if top == G.EOF:
                    break;
                cursor += 1
            else:
                production = M[top][a][0]
                output.append(production)
                production = list(production.Right)
                stack.extend(production[::-1])

        return output

    return parser

def metodo_predictivo_no_recursivo(G, M = None):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M)
    def updated(tokens):
        return parser([t.token_type for t in tokens])
    return updated

def get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode, ):
    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(UnaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.node, tabs + 1)
            return f'{ans}\n{child}'

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).token_type, EOF)
    return result

def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes

    synteticed = [None] * (len(body) + 1)
    inherited = [None] * (len(body) + 1)
    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            synteticed[i] = next(tokens).lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            attr = attributes[i]
            if attr is not None:
                inherited[i] = attr(inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])

    attr = attributes[0]
    if attr is None:
        return None
    return attr(inherited, synteticed)

def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            for item in automaton.transitions[state][symbol]:
            # aux = automaton.transitions[state][symbol]
                moves.add(item)
        except KeyError:
            pass
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p

    while pending:
        state = pending.pop()

        l = move(automaton, [state], '')
        for i in l:
            if(i in closure):
                pass
            else:
                closure.add(i)
                pending.append(i)

    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            new_state = move(automaton, state, symbol)
            new_state = epsilon_closure(automaton, new_state)

            if not new_state:
                continue

            for s in states:
                if(s == new_state):
                    new_state = s
                    break
            else:
                new_state.id = len(states)
                new_state.is_final = any(s in automaton.finals for s in new_state)
                pending.append(new_state)
                states.append(new_state)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = new_state.id

    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def automata_union(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        other = [q + d1 for q in destinations]
        transitions[origin + d1, symbol] = other

    for (origin, symbol), destinations in a2.map.items():
        other = [q + d2 for q in destinations]
        transitions[origin + d2, symbol] = other


    transitions[start, ''] = [a1.start + d1, a2.start + d2]
    for i in a1.finals:
        try:
            transitions[i + d1, ''].add(final)
        except KeyError:
            transitions[i + d1, ''] = [final]
    for i in a2.finals:
        try:
            transitions[i + d2, ''].add(final)
        except KeyError:
            transitions[i + d2, ''] = [final]

    states = a1.states + a2.states + 2
    finals = { final }

    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}

    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        other = [q + d1 for q in destinations]
        transitions[origin + d1, symbol] = other


    for (origin, symbol), destinations in a2.map.items():
        other = [q + d2 for q in destinations]
        transitions[origin + d2, symbol] = other

    for i in a1.finals:
        try:
            transitions[i + d1, ''].add(a2.start + d2)
        except KeyError:
            transitions[i + d1, ''] = [a2.start + d2]
    for i in a2.finals:
        try:
            transitions[i + d2, ''].append(final)
        except KeyError:
            transitions[i + d2, ''] = [final]

    states = a1.states + a2.states + 1
    finals = { final }

    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        other = [q + d1 for q in destinations]
        transitions[origin + d1, symbol] = other

    transitions[start, ''] = [final, a1.start + d1]

    for i in a1.finals:
        try:
            transitions[i + d1, ''].add(final)
        except KeyError:
            transitions[i + d1, ''] = [final]

    try:
        transitions[final, ''].add(start)
    except:
        transitions[final,''] = [start]

    states = a1.states +  2
    finals = { final }

    return NFA(states, finals, transitions, start)

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    transition = automaton.transitions

    for member in group:
        for item in split.keys():
            for symbol in vocabulary:
                q1 = None
                q2 = None
                try:
                    q1 = partition[transition[item][symbol][0]].representative
                except KeyError:
                    q1 = None
                try:
                    q2 = partition[transition[member.value][symbol][0]].representative
                except KeyError:
                    q2 = None
                if q1 != q2:
                    break
            else:
                split[item].append(member.value)
                break
        else:
            split[member.value] = [member.value]


    return [ group for group in split.values()]

def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))

    ## partition = { NON-FINALS | FINALS }
    finals = list(automaton.finals)
    non_finals = [state for state in range(automaton.states) if not state in automaton.finals]
    partition.merge(finals)
    partition.merge(non_finals)

    while True:
        new_partition = DisjointSet(*range(automaton.states))

        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        for group in partition.groups:
            new_groups = distinguish_states(group, automaton, partition)
            for new_group in new_groups:
                new_partition.merge(new_group)

        if len(new_partition) == len(partition):
            break

        partition = new_partition

    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)

    states = [s for s in partition.representatives]

    transitions = {}
    for i, state in enumerate(states):
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            new_dest = states.index(partition[destinations[0]].representative)

            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = new_dest
                pass

    start = states.index(partition[automaton.start].representative)
    finals = set([i for i in range(len(states)) if states[i].value in automaton.finals])

    return DFA(len(states), finals, transitions, start)


#methods to simplify the grammar
def remove_non_terminating_productions(G):
    terminals = set(G.terminals)

    change = True
    while change:
        change = False
        for prod in G.Productions:
            if prod.Left not in terminals and all([s in terminals for s in prod.Right]):
                terminals.add(prod.Left)
                change = True

    nt = G.nonTerminals.copy()
    G.nonTerminals = []
    G.Productions = []

    for s in nt:
        if s in terminals:
            G.nonTerminals.append(s)
            productions = s.productions.copy()
            s.productions = []
            for prod in productions:
                if all([item in terminals for item in prod.Right]):
                    G.Productions.append(prod)
                    s.productions.append(prod)

def remove_useless_productions(G):
    flag = [False] * (len(G.nonTerminals) + len(G.terminals))
    mp = {}

    for i, nt in enumerate(G.nonTerminals):
        mp[nt] = i
    sz = len(G.nonTerminals)
    for i, t in enumerate(G.terminals):
        mp[t] = i + sz

    def dfs(S):
        flag[mp[S]] = True
        for prod in S.productions:
            _, right = prod
            for symbol in right:
                if isinstance(symbol, Terminal):
                    flag[mp[symbol]] = True
                if isinstance(symbol, NonTerminal) and not flag[mp[symbol]]:
                    dfs(symbol)

    dfs(G.startSymbol)
    nt = G.nonTerminals.copy()
    G.nonTerminals = []
    G.Productions = []

    for item in nt:
        if flag[mp[item]]:
            G.nonTerminals.append(item)
            G.Productions.extend(item.productions)

    t = G.terminals.copy()
    G.terminals = []
    for item in t:
        if flag[mp[item]]:
            G.terminals.append(item)

def remove_null_productions(G):
    null_prod = set()

    change = True
    while change:
        change = False
        for prod in G.Productions:
            if prod.Left not in null_prod and all([s in null_prod for s in prod.Right]):
                null_prod.add(prod.Left)
                change = True
    if G.startSymbol in null_prod:
        return

    def add_prod(head, body, i, prod):
        if i == len(body):
            if len(prod) > 0:
                sentence = G.Epsilon
                for s in prod:
                    sentence += s
                head %= sentence
            return

        if body[i] not in null_prod:
            prod.append(body[i])
            add_prod(head, body, i + 1, prod)
            prod.pop()
        else:
            add_prod(head, body, i + 1, prod)
            prod.append(body[i])
            add_prod(head, body, i + 1, prod)
            prod.pop()

    G.Productions = []
    for nt in G.nonTerminals:
        nt_prod = nt.productions.copy()
        nt.productions = []
        for prod in nt_prod:
            head, body = prod.Left, prod.Right
            if any([s in null_prod for s in body]):
                production = []
                add_prod(head, body, 0, production)
            elif len(body) > 0:
                head %= body

    # if G.startSymbol in null_prod:
    #     G.startSymbol %= G.Epsilon

def remove_unit_productions(G):
    guf = {nt : set() for nt in G.nonTerminals}
    unit_prod = set()

    for prod in G.Productions:
        head, body = prod.Left, prod.Right
        if len(body) == 1 and isinstance(body[0], NonTerminal):
            unit_prod.add(prod)
        else:
            guf[head].add(body)

    change = True
    while change:
        change = False
        for prod in unit_prod:
            head, body = prod.Left, prod.Right
            sz = len(guf[head])
            #guf[head].update(guf[body[0]])
            for item in guf[body[0]]:
                if not item:
                    guf[head].add(G.Epsilon)
                else:
                    guf[head].add(item)
            change |= (sz < len(guf[head]))

    G.Productions = []
    for nt in G.nonTerminals:
        nt.productions = []
        for item in guf[nt]:
            nt %= item


def remove_common_prefix(G):
    unsolved = set([nt for nt in G.nonTerminals])

    id = 1
    while unsolved:
        nonTerminals = G.nonTerminals.copy()
        for nt in nonTerminals:
            if nt in unsolved:
                nt_prod = nt.productions.copy()
                nt.productions = []
                flag = set()

                for item in nt_prod:
                    if item not in flag:
                        flag.add(item)
                        if not item.IsEpsilon:
                            common = set()
                            symbols = []
                            s = item.Right[0]
                            symbols.append(s)
                            for p in nt_prod:
                                if p not in flag and len(p.Right) > 0:
                                    if p.Right[0] == s:
                                        flag.add(p)
                                        common.add(p)
                            if len(common) == 0:
                                item.Left %= item.Right
                            else:
                                for i in range(1, len(item.Right)):
                                    for c in common:
                                        if i == len(c.Right) or c.Right[i] != item.Right[i]:
                                            break
                                    else:
                                        symbols.append(item.Right[i])
                                        continue
                                    break
                                sentence = G.Epsilon
                                for symbol in symbols:
                                    sentence += symbol
                                new_nt = G.NonTerminal(nt.Name + '_' + str(id))
                                id += 1
                                nt %= sentence + new_nt
                                common.add(item)
                                for c in common:
                                    sent = G.Epsilon
                                    for i in range(len(symbols), len(c.Right)):
                                        sent += c.Right[i]
                                    new_nt %= sent
                                unsolved.add(new_nt)
                        else:
                            item.Left %= item.Right

                unsolved.remove(nt)

    G.Productions = []
    for nt in G.nonTerminals:
        for p in nt.productions:
            G.Productions.append(p)

def remove_immediate_recursion(G):
    G.Productions = []

    non_terminals = G.nonTerminals.copy()
    for item in non_terminals:
        bad_prod = [Sentence(*prod.Right[1:]) for prod in item.productions if len(prod.Right) > 0 and prod.Right[0] == item]
        good_prod = [Sentence(*prod.Right) for prod in item.productions if len(prod.Right) == 0 or prod.Right[0] != item]

        if len(bad_prod) > 0:
            nsymbol = G.NonTerminal(item.Name + '_0')
            item.productions = []

            for prod in good_prod:
                item %= prod + nsymbol

            for prod in bad_prod:
                nsymbol %= prod + nsymbol

            nsymbol %= G.Epsilon

        else:
            G.Productions.extend(item.productions)

def grammar_from_input(input):
    terminals, nonTerminals, productions = [], [], []

    input = input.split('\n')
    lines = [l for l in input if l != '']

    l = lines[0].split()
    start_symbol = l[-1]
    nonTerminals.append(start_symbol)

    l = lines[1].replace(',', ' ').split()
    if len(l) > 4:
        for i in range(3, len(l) - 1):
            nonTerminals.append(l[i])

    l = lines[2].replace(',', ' ').split()
    if len(l) > 4:
        for i in range(3, len(l) - 1):
            terminals.append(l[i])
    else:
        raise Exception('Invalid sentence')

    lines = lines[3:]
    for prod in lines:
        right, sentences = prod.split('=')
        right, = right.split()

        sentences = sentences.split(';')
        # sentences = sentences.split('|')
        for s in sentences:
            s = s.replace('+', ' ').split()
            # s = s.split()
            productions.append({'Head': right, 'Body': s})

    d = dict()
    d['NonTerminals'] = nonTerminals
    d['Terminals'] = terminals
    d['Productions'] = productions

    G = Grammar.from_json(json.dumps(d))

    if G.startSymbol is None:
        for nt in G.nonTerminals:
            if nt.Name == start_symbol:
                G.startSymbol = nt
                break

    return G

def simplifying_grammar(G):
    remove_null_productions(G)
    remove_unit_productions(G)
    remove_non_terminating_productions(G)
    remove_useless_productions(G)
    remove_immediate_recursion(G)
    remove_common_prefix(G)



def validate_conflict(w, M, G):
    stack =  [G.EOF, G.startSymbol]
    cursor = 0

    while True:
        top = stack.pop()
        a = w[cursor]

        if top.IsEpsilon:
            pass
        elif top.IsTerminal:
            assert top == a
            if top == G.EOF:
                break;
            cursor += 1
        else:
            if len(M[top][a]) > 1:
                return True
            production = M[top][a][0]
            production = list(production.Right)
            stack.extend(production[::-1])

    return False

def ll1_conflict(G, M):
    queue = []

    queue.append(([G.startSymbol], [], False))
    while queue:
        prod, word, conflict = queue.pop(0)
        while prod and isinstance(prod[0], Terminal):
            word.append(prod.pop(0))

        if not prod:
            if conflict:
                if validate_conflict(word + [G.EOF], M, G):
                    w = ' '.join([symbol.Name for symbol in word])
                    return w
            continue

        symbol = prod.pop(0)
        for terminal in M[symbol]:
            c = conflict or len(M[symbol][terminal]) > 1
            for p in M[symbol][terminal]:
                body = list(p.Right)
                body.extend(prod)
                queue.append((body, word.copy(), c))



def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [start_item]
    visited = {start_item: automaton}

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        # Your code here!!! (Decide which transitions to add)
        transitions = []

        next_item = current_item.NextItem()
        if next_item not in visited:
            visited[next_item] = State(next_item, True)
            pending.append(next_item)
        transitions.append(visited[next_item])

        symbol = current_item.NextSymbol
        if symbol.IsNonTerminal:
            for prod in symbol.productions:
                item = Item(prod, 0)
                if item not in visited:
                    visited[item] = State(item, True)
                    pending.append(item)
                transitions.append(visited[item])

        current_state = visited[current_item]
        # Your code here!!! (Add the decided transitions)
        current_state.add_transition(current_item.NextSymbol.Name, transitions[0])
        for item in transitions[1:]:
            current_state.add_epsilon_transition(item)
    return automaton

class SLR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        self.ok = True
        G = self.Augmented = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        self.automaton = build_LR0_automaton(G).to_deterministic(lambda x: "")
        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, node)
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self.ok &= upd_table(self.action, idx, G.EOF, (SLR1Parser.OK, ''))
                    else:
                        for terminal in follows[item.production.Left]:
                            self.ok &= upd_table(self.action, idx, terminal, (SLR1Parser.REDUCE, item.production))
                else:
                    symbol = item.NextSymbol

                    if symbol.IsTerminal:
                        self.ok &= upd_table(self.action, idx, symbol, (SLR1Parser.SHIFT, node[symbol.Name][0].idx))
                    else:
                        self.ok &= upd_table(self.goto, idx, symbol, node[symbol.Name][0].idx)

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    # Your code here!!! (Compute lookahead for child items)
    for preview in item.Preview():
        lookaheads.hard_update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    # Your code here!!! (Build and return child items)
    return [Item(prod, 0, lookaheads) for prod in next_symbol.productions]

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            # Your code here!!! (Get/Build `next_state`)
            items = current_state.state
            kernel = goto_lr1(items, symbol, just_kernel=True)
            if not kernel:
                continue
            try:
                next_state = visited[kernel]
            except KeyError:
                closure = goto_lr1(items, symbol, firsts)
                next_state = visited[kernel] = State(frozenset(closure), True)
                pending.append(kernel)

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(lambda x: "")
    return automaton

class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        self.ok = True
        G = self.Augmented = self.G.AugmentedGrammar(True)

        automaton = self.automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
            node.tag = f'I{i}'

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == G.startSymbol:
                        self.ok &= upd_table(self.action, idx, G.EOF, (ShiftReduceParser.OK, ''))
                    else:
                        for lookahead in item.lookaheads:
                            self.ok &= upd_table(self.action, idx, lookahead, (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.ok &= upd_table(self.action, idx, next_symbol, (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        self.ok &= upd_table(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)

def mergue_items_lookaheads(items, others):
    if len(items) != len(others):
        return False

    new_lookaheads = []
    for item in items:
        for item2 in others:
            if item.Center() == item2.Center():
                new_lookaheads.append(item2.lookaheads)
                break
        else:
            return False

    for item, new_lookahead in zip(items, new_lookaheads):
        item.lookaheads = item.lookaheads.union(new_lookahead)

    return True

def build_LALR1_automaton(G):
    lr1_automaton  = build_LR1_automaton(G)
    states = list(lr1_automaton)
    new_states = []
    visited = {}

    for i, state in enumerate(states):
        if state not in visited:
            # creates items
            items = [item.Center() for item in state.state]

            # check for states with same center
            for state2 in states[i:]:
                if mergue_items_lookaheads(items, state2.state):
                    visited[state2] = len(new_states)

            # add new state
            new_states.append(State(frozenset(items), True))

    # making transitions
    for state in states:
        new_state = new_states[visited[state]]
        for symbol, transitions in state.transitions.items():
            for state2 in transitions:
                new_state2 = new_states[visited[state2]]
                # check if the transition already exists
                if symbol not in new_state.transitions or new_state2 not in new_state.transitions[symbol]:
                    new_state.add_transition(symbol, new_state2)

    new_states[0].set_formatter(empty_formatter)
    return new_states[0]

class LALR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        self.ok = True
        G = self.Augmented = self.G.AugmentedGrammar(True)

        automaton = self.automaton = build_LALR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
            node.tag = f'I{i}'

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == G.startSymbol:
                        self.ok &= upd_table(self.action, idx, G.EOF, (ShiftReduceParser.OK, ''))
                    else:
                        for lookahead in item.lookaheads:
                            self.ok &= upd_table(self.action, idx, lookahead, (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.ok &= upd_table(self.action, idx, next_symbol, (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        self.ok &= upd_table(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)



def action_goto_conflict(action, goto):
    # (stack, word, conflict, terminal)
    queue = [([0], [], False, None)]

    while queue:
        stack, word, conflict, terminal = queue.pop(0)
        state = stack[-1]
        try:
            if terminal is not None:
                actions = action[state][terminal]
                if any([act for act, _ in actions if act == SLR1Parser.OK]) and conflict:
                    return ' '.join(word)

                conflict |= (len(actions) > 1)
                for act, tag in actions:
                    if act == SLR1Parser.SHIFT:
                        queue.append((stack + [tag], word + [terminal.Name], conflict, None))
                    elif act == SLR1Parser.REDUCE:
                        s = stack.copy()
                        if not tag.IsEpsilon:
                            s = s[:-len(tag.Right)]
                        data = goto[s[-1]][tag.Left]
                        c = (len(data) > 1) or conflict
                        for go in data:
                            queue.append((s + [go], word.copy(), c, terminal))
            else:
                for symbol in action[state]:
                    queue.append((stack, word.copy(), conflict, symbol))
        except Exception as e:
            print(f'FAILURE {e}')


# def action_goto_conflict(action, goto):
#     # (stack, word, conflict, terminal)
#     queue = [([0], '', False, None)]

#     while queue:
#         stack, word, conflict, terminal = queue.pop(0)
#         state = stack[-1]
#         try:
#             if terminal is not None:
#                 actions = action[state][terminal]
#                 if any([act for act, _ in actions if act == SLR1Parser.OK]) and conflict:
#                     return word

#                 conflict |= (len(actions) > 1)
#                 for act, tag in actions:
#                     if act == SLR1Parser.SHIFT:
#                         queue.append((stack + [tag], word + terminal.Name, conflict, None))
#                     elif act == SLR1Parser.REDUCE:
#                         s = stack.copy()
#                         if not tag.IsEpsilon:
#                             s = s[:-len(tag.Right)]
#                         data = goto[s[-1]][tag.Left]
#                         c = (len(data) > 1) or conflict
#                         for go in data:
#                             queue.append((s + [go], word, c, terminal))
#             else:
#                 for symbol in action[state]:
#                     queue.append((stack, word, conflict, symbol))
#         except Exception as e:
#             print(f'FAILURE {e}')



def ll1_analysis(G):
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)

    M, ok  = build_parsing_table(G, firsts, follows)

    return firsts, follows, M, ok



def derivation_tree(d):
    def add_trans(cur, transitions):
        for symbol in transitions:
            if symbol.IsTerminal:
                cur.add_transition('', State(symbol, True))
            else:
                s = State(symbol, True)
                try:
                    old[symbol].append(s)
                except KeyError:
                    old[symbol] = [s]
                cur.add_transition('', s)
        if len(transitions) == 0:
            cur.add_transition('', State(transitions, True))

    p1 = d[0]
    old = {}
    root = State(p1.Left.Name, True)
    add_trans(root, p1.Right)

    for p in d[1:]:
        node = old[p.Left].pop()
        add_trans(node, p.Right)

    return root

def parse_string(G, word):
    m = {t.Name:t for t in G.terminals}
    word = word.split()
    w = [m[item] for item in word]
    w.append(G.EOF)
    return w

def make_tree_LL1(G, w, M, firsts, follows):
    try:
        w = parse_string(G, w)
        return derivation_tree(deprecated_metodo_predictivo_no_recursivo(G, M, firsts, follows)(w))
    except Exception as e:
        return 'String not recognized'

def make_tree(G, w, parser):
    try:
        w = parse_string(G, w)
        d = parser(w)
        d.reverse()
        return derivation_tree(d)

    except Exception as e:
        return "String not recognized"