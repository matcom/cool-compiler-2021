from parser_automatons import (
    build_LR0_automaton,
    build_LR1_automaton,
    build_LALR_automaton,
)
from methods import compute_firsts, compute_local_first, compute_follows
from cmp.automata import State
from errors import shift_reduce_error, invalid_sentence_error


class ShiftReduceParser:
    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self.automaton = self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []
        operations = []

        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose:
                print(stack, "<---||--->", w[cursor:])

            # Detect error
            try:
                action, tag = self.action[state, lookahead]
            except KeyError:
                raise invalid_sentence_error(
                    w,
                    cursor,
                    lookahead,
                    None,
                    "No transition available. Sentence given does not belong to the grammar",
                    output,
                    operations,
                )
            # Exception(
            #         "No transition available"
            #     )  # string does not belong to this grammar

            # Shift case
            if action == self.SHIFT:
                operations.append(action)
                stack.append(tag)
                cursor += 1

            # Reduce case
            elif action == self.REDUCE:
                operations.append(action)
                for _ in range(len(tag.Right)):
                    stack.pop()
                output.append(tag)
                stack.append(self.goto[stack[-1], tag.Left])

            # OK case
            elif action == self.OK:
                return output, operations
            # Invalid case
            else:
                raise invalid_sentence_error(
                    w,
                    cursor,
                    lookahead,
                    None,
                    "Invalid case. Sentence given does not belong to the grammar",
                )
                # raise Exception("Invalid case")
                # break

            if cursor >= len(w):  # or not stack
                raise invalid_sentence_error(
                    w,
                    cursor - 1,
                    lookahead,
                    None,
                    "Exceed word length while looking for a viable derivation. Sentence given does not belong to the grammar",
                )
            # raise Exception("Invalid sentence")


class SLR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                # - Filling `self.Action` and `self.Goto` according to `item`)
                # - Using `self._register(...)`)
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in follows[item.production.Left]:
                            self._register(
                                self.action,
                                (idx, symbol),
                                (self.REDUCE, item.production),
                            )
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(
                            self.action,
                            (idx, item.NextSymbol),
                            (self.SHIFT, node[item.NextSymbol.Name][0].idx),
                        )
                    else:
                        self._register(
                            self.goto,
                            (idx, item.NextSymbol),
                            node[item.NextSymbol.Name][0].idx,
                        )
        return automaton

    @staticmethod
    def _register(table, key, value):
        # assert (
        #     key not in table or table[key] == value
        # ), "Shift-Reduce or Reduce-Reduce conflict!!!"
        if key in table and table[key] != value:
            raise shift_reduce_error(table[key], value, "SLR")
        table[key] = value


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i

        # print("automatons states")
        for node in automaton:
            idx = node.idx
            for item in node.state:
                # print("item", item)
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in item.lookaheads:
                            self._register(
                                self.action,
                                (idx, symbol),
                                (self.REDUCE, item.production),
                            )
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(
                            self.action,
                            (idx, item.NextSymbol),
                            (self.SHIFT, node[item.NextSymbol.Name][0].idx),
                        )
                    else:
                        self._register(
                            self.goto,
                            (idx, item.NextSymbol),
                            node[item.NextSymbol.Name][0].idx,
                        )
        return automaton

    @staticmethod
    def _register(table, key, value):
        if key in table and table[key] != value:
            raise shift_reduce_error(table[key], value, "LR", key)
        table[key] = value


class LALR_Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LALR_automaton(G)

        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in item.lookaheads:
                            self._register(
                                self.action,
                                (idx, symbol),
                                (self.REDUCE, item.production),
                            )
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(
                            self.action,
                            (idx, item.NextSymbol),
                            (self.SHIFT, node[item.NextSymbol.Name][0].idx),
                        )
                    else:
                        self._register(
                            self.goto,
                            (idx, item.NextSymbol),
                            node[item.NextSymbol.Name][0].idx,
                        )

        return automaton

    @staticmethod
    def _register(table, key, value):
        if key in table and table[key] != value:
            raise shift_reduce_error(table[key], value, "LALR")
        table[key] = value


# ----------------------derivation tree-------------------------#
def DerivationTree(derivation, G):
    lent = len(derivation)

    nonTerminalstack = []
    root = State(G.startSymbol.Name)
    nonTerminalstack.append(root)

    while lent > 0:
        lent -= 1
        next_production = derivation[lent]
        print("next_production", next_production)
        currentNode = nonTerminalstack.pop()
        # assert currentNode.state == next_production.Left.Name, "Wrong derivation"

        if next_production.IsEpsilon:
            currentNode.add_transition(" ", State("epsilon", True))

        for symbol in next_production.Right:
            if symbol.IsTerminal:
                currentNode.add_transition(" ", State(symbol.Name, True))
            else:
                nonTerminalstack.append(State(symbol.Name))
                currentNode.add_transition(
                    " ", nonTerminalstack[len(nonTerminalstack) - 1]
                )

    return root
