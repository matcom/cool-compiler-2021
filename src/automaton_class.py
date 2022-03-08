from collections import deque
from itertools import repeat, chain
from typing import Set, Union
from state_class import State


class Automaton:
    def __init__(self):
        self.start: Union[State, None] = None
        self.states: Set[State] = set()
        self.finals: Set[State] = set()
        self.counter = 1

    def add_state(self, *states):
        for state in states:
            state: State
            # no named
            if state.name is None:
                state.name = self.counter
                self.counter += 1

            if state in self.states:
                state.name += self.counter
                self.counter += 1
                self.add_state(state)

            if self.start is None:
                self.start = state
            if state.final:
                self.finals.add(state)
            self.states.add(state)

    def copy(self, n_st_a=None):
        automaton = Automaton()
        states_dic = dict()

        def create_state(state):
            st = states_dic.get(state, None)
            if st is None:
                st = state.copy(n_st_a)
                states_dic[state] = st
                automaton.add_state(st)
            return st

        for state in self.states:
            st = create_state(state)
            for s, to in chain(
                state.transitions.items(), zip(repeat(None), state.epsilon_transitions)
            ):
                n_dest = create_state(to)
                st[s] = n_dest
        automaton.start = states_dic[self.start]
        return automaton

    def upd_stars(self):
        a = self.copy()
        for final in a.finals:
            a.start[None] = final
        return a

    def upd_finals(self):
        a = self.copy()
        for final in a.finals:
            final[None] = a.start
        return a

    def dfa_contructor(self):
        b = True
        for state in self.states:
            if len(state.epsilon_transitions):
                b = False
                break
        if b:
            return self
        return self.to_deterministic(
            [self.start],
            self.goto,
            self.epsilon_closure,
            self.state_constr,
            self.vocabulary,
        )

    @staticmethod
    def to_deterministic(
        start_value, goto_func, closure_func, state_constr, vocabulary_f
    ):
        dfa = Automaton()
        start = closure_func(start_value)  # q0
        start_state = state_constr(start)
        dfa.add_state(start_state)

        states_list = {start: start_state}
        pending = deque([start])

        while pending:
            clousure_state = pending.popleft()
            state = states_list[clousure_state]
            s_vocabulary = vocabulary_f(clousure_state)
            for symbol in s_vocabulary:
                goto = goto_func(clousure_state, symbol)
                clousure = closure_func(goto)
                new_state = states_list.get(clousure, None)

                if new_state is None:
                    pending.append(clousure)
                    new_state = state_constr(clousure)
                    dfa.add_state(new_state)
                    states_list[clousure] = new_state

                state[symbol] = new_state
        return dfa

    @staticmethod
    def goto(states, symbol):
        goto = set()
        for state in states:
            if state[symbol]:
                goto.add(state[symbol])
        return tuple(sorted(goto, key=hash))

    @staticmethod
    def epsilon_closure(states):
        pending = list(states)
        clousure = set()
        while pending:
            state: State = pending.pop()
            clousure.add(state)
            for elem in state.epsilon_transitions:
                if elem not in clousure:
                    pending.append(elem)
        return tuple(sorted(clousure, key=hash))

    @staticmethod
    def state_constr(to_sum):
        return sum(to_sum)

    @staticmethod
    def vocabulary(states):
        return sorted(
            set(chain.from_iterable(x.trans_symbols() for x in states)), key=hash
        )

    def __add__(self, other: "Automaton") -> "Automaton":
        n_st_a = len(self.states) + len(other.states)
        s_copy = self.copy(n_st_a)
        o_copy = other.copy(n_st_a * 2)

        for final in s_copy.finals:  # f = f1 ∪ f2∪ . . .
            final[None] = o_copy.start
            final.final = False

        s_copy.finals.clear()
        s_copy.add_state(*o_copy.states)  # Q = Q1 ∪ Q2 ∪ {q0, qf}
        return s_copy  # q0 = q0, F = {qf}

    def __or__(self, other: "Automaton") -> "Automaton":
        n_st_a = len(self.states) + len(other.states)
        s_copy = self.copy(n_st_a)
        o_copy = other.copy(n_st_a * 2)
        s_copy.add_state(*o_copy.states)

        start_state = State()
        s_copy.add_state(start_state)
        start_state[None] = s_copy.start
        start_state[None] = o_copy.start
        s_copy.start = start_state
        return s_copy
