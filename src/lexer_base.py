from typing import List

from token_class import Token, tokenizer
from match_class import Match
from serializer_class import Serializer


class LexerTable(list, Serializer):
    def __init__(self, ignore, eof, eoline):
        super(LexerTable, self).__init__()
        self.ignore = ignore
        self.eof = eof
        self.eoline = eoline


class Lexer:
    def __init__(self, match: Match, token_type=None):
        if token_type:
            globals()["TOKEN_TYPE"] = token_type

        self.table: LexerTable = LexerTable.deserializer("--LEXER--")
        self.match: Match = match
        for t in self.table:
            if t[0] != self.table.eof:
                self.match.add_matcher(t)
        self.match.initialize()

    def __call__(self, input: str) -> List[Token]:
        token_list, errors = tokenizer(
            input, self.table.ignore, self.table.eof, self.table.eoline, self.match
        )
        return token_list, errors
