from parsers import parser_shr, ParserTable


class Parser:
    def __init__(self, ast_class, token_type=None):
        if token_type:
            globals()["TOKEN_TYPE"] = token_type

        self.ast_class = ast_class
        self.table: ParserTable = ParserTable.deserializer("--PARSER--")

    def __call__(self, tokens_list):
        return parser_shr(tokens_list, self.ast_class, self.table, attr_decoder)


def attr_decoder(self, attr, symbols_to_reduce, ast_class):
    pass
