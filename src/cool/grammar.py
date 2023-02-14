import inspect
import time

from pyjapt import Grammar, Lexer, ShiftReduceParser, Token

import cool.semantics.utils.astnodes as cool

G = Grammar()

#################
# Non-Terminals #
#################
program = G.add_non_terminal("program", start_symbol=True)
class_list = G.add_non_terminal("class-list")
class_def = G.add_non_terminal("class-def")
feature_list = G.add_non_terminal("feature-list")
attribute = G.add_non_terminal("attribute")
method = G.add_non_terminal("method")
param_list = G.add_non_terminal("param-list")
block = G.add_non_terminal("block")
declaration_list = G.add_non_terminal("declaration-list")
case_list = G.add_non_terminal("case-list")
function_call = G.add_non_terminal("function-call")
expr_list = G.add_non_terminal("expr-list")
not_empty_expr_list = G.add_non_terminal("not-empty-expr-list")
expr = G.add_non_terminal("expr")
negable_comp = G.add_non_terminal("negable-comp")
comp = G.add_non_terminal("comp")
negable_arith = G.add_non_terminal("negable-arith")
arith = G.add_non_terminal("arith")
term = G.add_non_terminal("term")
factor = G.add_non_terminal("factor")
atom = G.add_non_terminal("atom")

###########
# Symbols #
###########
G.add_terminals("{ } ( ) . , : ; @ <- =>")

############
# Keywords #
############
keywords = G.add_terminals(
    "class inherits if then else fi while loop pool let in case of esac new isvoid true false not"
)
keywords_names = {x.name for x in keywords}

#############
# Symbols #
#############
G.add_terminals("+ - * / < <= = ~")


###############
# Identifiers #
###############
@G.terminal("id", r"[a-z][a-zA-Z0-9_]*")
def id_terminal(lexer: Lexer):
    lex = lexer.token.lex
    lexer.column += len(lex)
    lexer.position += len(lex)
    lexer.token.token_type = (
        lex.lower() if lex.lower() in keywords_names else lexer.token.token_type
    )
    return lexer.token


@G.terminal("type", regex=r"[A-Z][a-zA-Z0-9_]*")
def type_terminal(lexer: Lexer):
    lex = lexer.token.lex
    lexer.column += len(lex)
    lexer.position += len(lex)
    lexer.token.token_type = (
        lex.lower()
        if lex.lower() in keywords_names - {"true", "false"}
        else lexer.token.token_type
    )
    return lexer.token


###############
# Basic Types #
###############
G.add_terminal("int", regex=r"\d+")


@G.terminal("string", regex=r"\"")
def string(lexer: Lexer):
    text = lexer.text
    pos = lexer.position + 1
    lexer.column += 1
    lex = '"'

    contains_null_character = False
    while True:
        if pos >= len(text):
            lexer.contain_errors = True
            lexer.position = pos
            lexer.add_error(
                lexer.lineno,
                lexer.column,
                f"({lexer.lineno}, {lexer.column}) - LexicographicError: EOF in string constant",
            )
            return

        s = text[pos]

        if s == "\\":
            if text[pos + 1] == "\n":
                lex += "\n"
                pos += 2
                lexer.lineno += 1
                lexer.column = 1
            elif text[pos + 1] in ("b", "f", "t", "n"):
                if text[pos + 1] == "b":
                    lex += "\\b"
                elif text[pos + 1] == "f":
                    lex += "\\f"
                elif text[pos + 1] == "t":
                    lex += "\\t"
                else:
                    lex += "\\n"

                pos += 2
                lexer.column += 2
            else:
                lex += text[pos + 1]
                pos += 2
                lexer.column += 2
        elif s == "\n":
            # Unterminated String
            lexer.contain_errors = True
            lexer.position = pos
            lexer.add_error(
                lexer.lineno,
                lexer.column,
                f"({lexer.lineno}, {lexer.column}) - LexicographicError: Unterminated string constant",
            )
            return
        elif s == "\0":
            contains_null_character = True
            lexer.contain_errors = True
            lexer.add_error(
                lexer.lineno,
                lexer.column,
                f"({lexer.lineno}, {lexer.column}) - LexicographicError: String contains null character",
            )
            pos += 1
            lexer.column += 1
        else:
            lex += s
            pos += 1
            lexer.column += 1

            if s == '"':
                break

    lexer.position = pos
    lexer.token.lex = lex
    if not contains_null_character:
        return lexer.token


############
# Comments #
############
@G.terminal("single_line_comment", r"--.*")
def single_line_comment(lexer):
    lex = lexer.token.lex
    for s in lex:
        if s == "\n":
            lexer.lineno += 1
            lexer.column = 0
        lexer.column += 1
    lexer.position += len(lex)


@G.terminal("multi_line_comment", r"\(\*")
def multi_line_comment(lexer: Lexer):
    counter = 1
    text = lexer.text
    pos = lexer.position + 2
    lexer.column += 2
    lex = "(*"

    while counter > 0:
        if pos >= len(text):
            lexer.contain_errors = True
            lexer.position = pos
            lexer.add_error(
                lexer.lineno,
                lexer.column,
                f"({lexer.lineno}, {lexer.column}) - LexicographicError: EOF in comment",
            )
            return None

        if text.startswith("(*", pos):
            counter += 1
            pos += 2
            lex += "(*"
            lexer.column += 2
        elif text.startswith("*)", pos):
            counter -= 1
            pos += 2
            lex += "*)"
            lexer.column += 2
        else:
            if text[pos] == "\n":
                lexer.lineno += 1
                lexer.column = 0
            elif text[pos] == "\t":
                lexer.column += 3
            lex += text[pos]
            pos += 1
            lexer.column += 1
    lexer.position = pos
    lexer.token.lex = lex


##################
# Ignored Tokens #
##################
@G.terminal("newline", r"\n+")
def newline(lexer: Lexer):
    lexer.lineno += len(lexer.token.lex)
    lexer.position += len(lexer.token.lex)
    lexer.column = 1


@G.terminal("whitespace", r" +")
def whitespace(lexer):
    lexer.column += len(lexer.token.lex)
    lexer.position += len(lexer.token.lex)


@G.terminal("tabulation", r"\t+")
def tab(lexer):
    lexer.column += 4 * len(lexer.token.lex)
    lexer.position += len(lexer.token.lex)


@G.lexical_error
def lexical_error(lexer):
    lexer.add_error(
        lexer.lineno,
        lexer.column,
        f'({lexer.lineno}, {lexer.column}) - LexicographicError: ERROR "{lexer.token.lex}"',
    )
    lexer.column += len(lexer.token.lex)
    lexer.position += len(lexer.token.lex)


###############
# Productions #
###############
program %= "class-list", lambda s: cool.ProgramNode(s[1])

class_list %= "class-def ;", lambda s: [s[1]]
class_list %= "class-def ; class-list", lambda s: [s[1]] + s[3]

class_def %= "class type { feature-list }", lambda s: cool.ClassDeclarationNode(
    s[2], s[4]
)
class_def %= (
    "class type inherits type { feature-list }",
    lambda s: cool.ClassDeclarationNode(s[2], s[6], s[4]),
)

feature_list %= "", lambda s: []
feature_list %= "attribute ; feature-list", lambda s: [s[1]] + s[3]
feature_list %= "method ; feature-list", lambda s: [s[1]] + s[3]

attribute %= "id : type", lambda s: cool.AttrDeclarationNode(s[1], s[3])
attribute %= "id : type <- expr", lambda s: cool.AttrDeclarationNode(s[1], s[3], s[5])

method %= "id ( ) : type { expr }", lambda s: cool.MethodDeclarationNode(
    s[1], [], s[5], s[7]
)
method %= "id ( param-list ) : type { expr }", lambda s: cool.MethodDeclarationNode(
    s[1], s[3], s[6], s[8]
)

param_list %= "id : type", lambda s: [(s[1], s[3])]
param_list %= "id : type , param-list", lambda s: [(s[1], s[3])] + s[5]

expr %= "id <- expr", lambda s: cool.AssignNode(s[1], s[3])
expr %= "{ block }", lambda s: cool.BlockNode(s[2])
expr %= "while expr loop expr pool", lambda s: cool.WhileNode(s[2], s[4])
expr %= "let declaration-list in expr", lambda s: cool.LetNode(s[2], s[4])
expr %= "case expr of case-list esac", lambda s: cool.SwitchCaseNode(s[2], s[4])
expr %= "negable-comp", lambda s: s[1]

negable_comp %= "not comp", lambda s: cool.NegationNode(s[2])
negable_comp %= "comp", lambda s: s[1]

comp %= "comp < negable-arith", lambda s: cool.LessThanNode(s[1], s[2], s[3])
comp %= "comp <= negable-arith", lambda s: cool.LessEqualNode(s[1], s[2], s[3])
comp %= "comp = negable-arith", lambda s: cool.EqualNode(s[1], s[2], s[3])
comp %= "arith", lambda s: s[1]

negable_arith %= "not arith", lambda s: cool.NegationNode(s[2])
negable_arith %= "arith", lambda s: s[1]

arith %= "arith + term", lambda s: cool.PlusNode(s[1], s[2], s[3])
arith %= "arith - term", lambda s: cool.MinusNode(s[1], s[2], s[3])
arith %= "term", lambda s: s[1]

term %= "term * factor", lambda s: cool.StarNode(s[1], s[2], s[3])
term %= "term / factor", lambda s: cool.DivNode(s[1], s[2], s[3])
term %= "factor", lambda s: s[1]

factor %= "isvoid factor", lambda s: cool.IsVoidNode(s[2])
factor %= "~ factor", lambda s: cool.ComplementNode(s[2])
factor %= "atom", lambda s: s[1]

atom %= "id", lambda s: cool.VariableNode(s[1])
atom %= "true", lambda s: cool.BooleanNode(s[1])
atom %= "false", lambda s: cool.BooleanNode(s[1])
atom %= "int", lambda s: cool.IntegerNode(s[1])
atom %= "string", lambda s: cool.StringNode(s[1])
atom %= "if expr then expr else expr fi", lambda s: cool.ConditionalNode(s[2], s[4], s[6])
atom %= "function-call", lambda s: s[1]
atom %= "new type", lambda s: cool.InstantiateNode(s[2])
atom %= "( expr )", lambda s: s[2]

block %= "expr ;", lambda s: [s[1]]
block %= "expr ; block", lambda s: [s[1]] + s[3]

declaration_list %= "id : type", lambda s: [(s[1], s[3], None)]
declaration_list %= "id : type <- expr", lambda s: [(s[1], s[3], s[5])]
declaration_list %= "id : type , declaration-list",lambda s: [(s[1], s[3], None)] + s[5]
declaration_list %= "id : type <- expr , declaration-list",lambda s: [(s[1], s[3], s[5])] + s[7]

case_list %= "id : type => expr ;", lambda s: [(s[1], s[3], s[5])]
case_list %= "id : type => expr ; case-list", lambda s: [(s[1], s[3], s[5])] + s[7]

function_call %= "id ( expr-list )", lambda s: cool.MethodCallNode(s[1], s[3])
function_call %= "atom . id ( expr-list )", lambda s: cool.MethodCallNode(s[3], s[5], s[1])
function_call %= "atom @ type . id ( expr-list )", lambda s: cool.MethodCallNode(s[5], s[7], s[1], s[3])

expr_list %= "", lambda s: []
expr_list %= "not-empty-expr-list", lambda s: s[1]
not_empty_expr_list %= "expr", lambda s: [s[1]]
not_empty_expr_list %= "expr , not-empty-expr-list", lambda s: [s[1]] + s[3]

#####################
# Error Productions #
#####################
G.add_terminal_error()


@G.parsing_error
def parsing_error(parser: ShiftReduceParser):
    t = parser.current_token
    parser.add_error(
        t.line,
        t.column,
        f'({t.line}, {t.column}) - SyntacticError: ERROR at or near "{t.lex}"',
    )


@G.production("feature-list -> attribute error feature-list")
def feature_attribute_error(s):
    s.add_error(
        2,
        f'({s[2].line}, {s[2].column}) - SyntacticError: ERROR at or near "{s[2].lex}"',
    )
    return [s[1]] + s[3]


@G.production("feature-list -> method error feature-list")
def feature_method_error(s):
    s.add_error(
        2,
        f'({s[2].line}, {s[2].column}) - SyntacticError: ERROR at or near "{s[2].lex}"',
    )
    return [s[1]] + s[3]


@G.production("case-list -> id : type => expr error")
def case_list_error(s):
    s.add_error(
        6,
        f'({s[6].line}, {s[6].column}) - SyntacticError: ERROR at or near "{s[6].lex}"',
    )
    return [(s[1], s[3], s[5])]


@G.production("case-list -> id : type => expr error case-list")
def case_list_error(s):
    s.add_error(
        6,
        f'({s[6].line}, {s[6].column}) - SyntacticError:ERROR at or near "{s[6].lex}"',
    )
    return [(s[1], s[3], s[5])] + s[7]


@G.production("block -> expr error")
def block_single_error(s):
    s.add_error(
        2,
        f'({s[2].line}, {s[2].column}) - SyntacticError: ERROR at or near "{s[2].lex}"',
    )
    return [s[1]]


@G.production("block -> expr error block")
def block_single_error(s):
    s.add_error(
        2,
        f'({s[2].line}, {s[2].column}) - SyntacticError: ERROR at or near "{s[2].lex}"',
    )
    return [s[1]] + s[3]


#################
# Serialize API #
#################
def serialize_parser_and_lexer():
    import typer

    t = time.time()
    G.serialize_lexer("CoolLexer", inspect.getmodulename(__file__))
    G.serialize_parser("lalr1", "CoolParser", inspect.getmodulename(__file__))

    styled_e = typer.style(
        f"Serialization Time : {time.time() - t} seconds",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.echo(styled_e)


if __name__ == "__main__":
    serialize_parser_and_lexer()
