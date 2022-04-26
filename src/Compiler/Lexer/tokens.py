class COOL_Tokens:

    def __init__(self):
        self.tokens = self.cool_tokens + list(self.cool_keywords.values())

    @property
    def cool_tokens(self):
        """
        Collection of COOL Syntax Tokens.
        :return: Tuple.
        """
        return [
            # Identifiers
            "ID", "TYPE",
            # Primitive Types
            "INTEGER", "STRING", "BOOLEAN",
            # Literals
            "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "COMMA", "DOT", "SEMICOLON", "AT",
            # Operators
            "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", "INT_COMP",
            # Special Operators
            "ARROW"
        ]
    
    @property
    def cool_keywords(self):
        """
        Map of Basic-COOL reserved keywords.
        :return: dict.
        """
        return {
            "case": "CASE",
            "class": "CLASS",
            "else": "ELSE",
            "esac": "ESAC",
            "fi": "FI",
            "if": "IF",
            "in": "IN",
            "inherits": "INHERITS",
            "isvoid": "ISVOID",
            "let": "LET",
            "loop": "LOOP",
            "new": "NEW",
            "of": "OF",
            "not": "NOT",
            "pool": "POOL",
            "then": "THEN",
            "while": "WHILE"
        }