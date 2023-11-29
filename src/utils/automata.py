try:
    import pydot
except:
    pass


class State:
    def __init__(self, state, final=False, formatter=lambda x: str(x), shape='circle'):
        self.state = state
        self.final = final
        self.transitions = {}
        self.epsilon_transitions = set()
        self.tag = None
        self.formatter = formatter
        self.shape = shape

    # The method name is set this way from compatibility issues.
    def set_formatter(self, value, attr='formatter', visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        self.__setattr__(attr, value)
        for destinations in self.transitions.values():
            for node in destinations:
                node.set_formatter(value, attr, visited)
        for node in self.epsilon_transitions:
            node.set_formatter(value, attr, visited)
        return self

    def has_transition(self, symbol):
        return symbol in self.transitions

    def add_transition(self, symbol, state):
        try:
            self.transitions[symbol].append(state)
        except:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.add(state)
        return self

    def recognize(self, string):
        states = self.epsilon_closure
        for symbol in string:
            states = self.move_by_state(symbol, *states)
            states = self.epsilon_closure_by_state(*states)
        return any(s.final for s in states)

    def to_deterministic(self, formatter=lambda x: str(x)):
        closure = self.epsilon_closure
        start = State(tuple(closure), any(s.final for s in closure), formatter)

        closures = [closure]
        states = [start]
        pending = [start]

        while pending:
            state = pending.pop()
            symbols = {symbol for s in state.state for symbol in s.transitions}

            for symbol in symbols:
                move = self.move_by_state(symbol, *state.state)
                closure = self.epsilon_closure_by_state(*move)

                if closure not in closures:
                    new_state = State(tuple(closure), any(s.final for s in closure), formatter)
                    closures.append(closure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = closures.index(closure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return start

    @staticmethod
    def from_nfa(nfa, get_states=False):
        states = []
        for n in range(nfa.states):
            state = State(n, n in nfa.finals)
            states.append(state)

        for (origin, symbol), destinations in nfa.map.items():
            origin = states[origin]
            origin[symbol] = [states[d] for d in destinations]

        if get_states:
            return states[nfa.start], states
        return states[nfa.start]

    @staticmethod
    def move_by_state(symbol, *states):
        return {s for state in states if state.has_transition(symbol) for s in state[symbol]}

    @staticmethod
    def epsilon_closure_by_state(*states):
        closure = {state for state in states}

        l = 0
        while l != len(closure):
            l = len(closure)
            tmp = [s for s in closure]
            for s in tmp:
                for epsilon_state in s.epsilon_transitions:
                    closure.add(epsilon_state)
        return closure

    @property
    def epsilon_closure(self):
        return self.epsilon_closure_by_state(self)

    @property
    def name(self):
        return self.formatter(self.state)

    def get(self, symbol):
        target = self.transitions[symbol]
        assert len(target) == 1
        return target[0]

    def __getitem__(self, symbol):
        if symbol == '':
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None

    def __setitem__(self, symbol, value):
        if symbol == '':
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        yield from self._visit()

    def _visit(self, visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        yield self

        for destinations in self.transitions.values():
            for node in destinations:
                yield from node._visit(visited)
        for node in self.epsilon_transitions:
            yield from node._visit(visited)

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        visited = set()

        def visit(start):
            ids = id(start)
            if ids not in visited:
                visited.add(ids)
                G.add_node(pydot.Node(ids, label=start.name, shape=self.shape, style='bold' if start.final else ''))
                for tran, destinations in start.transitions.items():
                    for end in destinations:
                        visit(end)
                        G.add_edge(pydot.Edge(ids, id(end), label=tran, labeldistance=2))
                for end in start.epsilon_transitions:
                    visit(end)
                    G.add_edge(pydot.Edge(ids, id(end), label='ε', labeldistance=2))

        visit(self)
        G.add_edge(pydot.Edge('start', id(self), label='', style='dashed'))

        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

    # def write_to(self, fname):
    #     return self.graph().write_svg(fname)


def multiline_formatter(state):
    return '\n'.join(str(item) for item in state)


def lr0_formatter(state):
    try:
        return '\n'.join(str(item)[:-1] for item in state)
    except TypeError:
        return str(state)[:-1]  # this used to be -4


import pydot
from tools.utils import ContainerSet, DisjointSet


class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = {state: {} for state in range(states)}

        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)

        self.vocabulary.discard('')

    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass


class DFA(NFA):

    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)

        transitions = {key: [value] for key, value in transitions.items()}
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start

    def _move(self, symbol):
        try:
            self.current = self.transitions[self.current[0]][symbol]
            return True
        except KeyError:
            return False

    def _reset(self):
        self.current = self.start

    def recognize(self, string):
        self.current = [self.current]
        for char in string:
            if not self._move(char):
                self._reset()
                return False
        tmp = self.current[0]
        self._reset()
        return tmp in self.finals


def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            for new_state in automaton.transitions[state][symbol]:
                moves.add(new_state)
        except KeyError:
            pass
    return moves


def epsilon_closure(automaton, states):
    pending = [s for s in states]
    closure = {s for s in states}

    while pending:
        state = pending.pop()
        # Your code here
        for new_state in automaton.epsilon_transitions(state):
            closure.add(new_state)
            pending.append(new_state)

    return ContainerSet(*closure)


def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [start]

    pending = [start]
    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            goto = move(automaton, state, symbol)
            new_state = epsilon_closure(automaton, goto)
            if len(new_state) == 0:
                continue
            new_state.is_final = any(s in automaton.finals for s in new_state)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                new_id = 0
                for i, item in enumerate(states, 0):
                    if item.set.issubset(new_state.set) and new_state.set.issubset(item.set):
                        new_state.id = item.id
                        new_id = item.id
                        break
                else:
                    new_state.id = i + 1
                    pending.append(new_state)
                    states.append(new_state)
                    new_id = i + 1

                transitions[state.id, symbol] = new_id

    finals = [state.id for state in states if state.is_final]
    dfa = DFA(len(states), finals, transitions)
    return dfa


def automata_union(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        transitions[origin + d1, symbol] = [i + d1 for i in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[origin + d2, symbol] = [i + d2 for i in destinations]

    transitions[start, ''] = [d1, d2]

    for final_a1 in a1.finals:
        transitions[final_a1 + d1, ''] = [final]
    for final_a2 in a2.finals:
        transitions[final_a2 + d2, ''] = [final]

    states = a1.states + a2.states + 2
    finals = {final}

    return NFA(states, finals, transitions, start)


def automata_concatenation(a1, a2):
    transitions = {}

    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        transitions[origin, symbol] = destinations

    for (origin, symbol), destinations in a2.map.items():
        transitions[origin + d2, symbol] = [i + d2 for i in destinations]

    for final_a1 in a1.finals:
        transitions[final_a1, ''] = [d2]
    for final_a2 in a2.finals:
        transitions[final_a2 + d2, ''] = [final]

    states = a1.states + a2.states + 1
    finals = {final}

    return NFA(states, finals, transitions, start)


def automata_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        transitions[origin + d1, symbol] = {d + d1 for d in destinations}
    transitions[start, ''] = [a1.start + d1, final]

    for f in a1.finals:
        try:
            X = transitions[f + d1, '']
        except KeyError:
            X = transitions[f + d1, ''] = set()
        X.add(final)
        X.add(a1.start + d1)
    J = a1.states + 2
    S = {final}
    return NFA(J, S, transitions, start)


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

    return [group for group in split.values()]


def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))

    finals = list(automaton.finals)
    non_finals = [state for state in range(automaton.states) if not state in automaton.finals]
    partition.merge(finals)
    partition.merge(non_finals)

    while True:
        new_partition = DisjointSet(*range(automaton.states))

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
                transitions[i, symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = new_dest
                pass

    start = states.index(partition[automaton.start].representative)
    finals = set([i for i in range(len(states)) if states[i].value in automaton.finals])

    return DFA(len(states), finals, transitions, start)
