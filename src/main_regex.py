from typing import Dict

from automaton_class import Automaton
import ast_regex as ast
from lexer_regex import Lexer
from parser_regex import Parser
from match_class import Match


class RegexExpr:
    def __init__(self, automaton):
        self.automaton: Automaton = automaton

    def match(self, input, pos=0):
        len_input = len(input)
        current = self.automaton.start
        match = ""
        while pos < len_input:
            char = input[pos]
            if char not in current.transitions:
                break
            current = current[char]
            match += char
            pos += 1
        return (match, True) if current.final else (match, False)


class RegexCompilator:
    class SimpleMatch(Match):
        def __init__(self):
            self.match_: Dict[str, str] = dict()

        def add_matcher(self, to_add):
            self.match_[to_add[1]] = to_add[0]

        def initialize(self):
            pass

        def match(self, match, pos):
            to_match = match[pos]
            if to_match in self.match_:
                return (self.match_[to_match], to_match, (False, []), True)
            else:
                return (self.match_[""], to_match, (False, []), True)

    def __init__(self):
        self.tokenizer = Lexer(RegexCompilator.SimpleMatch())
        self.parser = Parser(ast)

    def compile(self, regex):
        regex_tokens, _ = self.tokenizer(regex)
        regex_ast, _ = self.parser(regex_tokens)
        nfa = regex_ast.shift()
        dfa = nfa.dfa_contructor()
        return RegexExpr(dfa)
