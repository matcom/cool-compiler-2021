from LR1 import *
from Utils import * 

class LALR1Parser(LR1Parser):
    @staticmethod
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

    def build_LR1_automaton(self):
        super().build_LR1_automaton()

        states = list(self.automaton)
        new_states = []
        visited = {}

        for i, state in enumerate(states):
            if state not in visited:
                # creates items
                items = [item.Center() for item in state.state]

                # check for states with same center
                for state2 in states[i:]:
                    if LALR1Parser.mergue_items_lookaheads(items, state2.state):
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
        self.automaton = new_states[0]