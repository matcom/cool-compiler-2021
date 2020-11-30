# https://www.dabeaz.com/ply/ply.html
# file for PLY rules

# Declare the state
states = (("comments", "exclusive"),)


# All lexers must provide a list tokens that defines all of the possible token names
# that can be produced by the lexer.
first_tokens = [
    "larrow",
    "rarrow",
    "lessequal",
    "id",
    "int",
    "string",
]

reserved = {
    "class": "class",
    "inherits": "inherits",
    "not": "not",
    "isvoid": "isvoid",
    "let": "let",
    "in": "in",
    "if": "if",
    "then": "then",
    "else": "else",
    "fi": "fi",
    "loop": "loop",
    "pool": "pool",
    "case": "case",
    "of": "of",
    "esac": "esac",
    "while": "while",
    "new": "new",
    "true": "true",
    "false": "false",
}

literals = [
    ";",
    ":",
    ",",
    ".",
    "(",
    ")",
    "{",
    "}",
    "@",
    "+",
    "-",
    "*",
    "/",
    "<",
    "=",
    "~",
]

tokens = first_tokens + list(reserved.values())

# Match the first (*. Enter comments state.
def t_comments(t):
    r"\(\*"
    t.lexer.code_start = t.lexer.lexpos  # Record the starting position
    t.lexer.level = 1  # Initial level
    t.lexer.begin("comments")  # Enter 'comments' state


# Rules for the comments state
# Comments starting symbol
def t_comments_opsymb(t):
    r"\(\*"
    t.lexer.level += 1


# Comments closing symbol
def t_comments_clsymb(t):
    r"\*\)"
    t.lexer.level -= 1

    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.code_start : t.lexer.lexpos + 1]
        t.lexer.lineno += t.value.count("\n")
        t.lexer.begin("INITIAL")


# For bad characters. In this case we just skip over everything but (* or *)
def t_comments_error(t):
    t.lexer.skip(1)


# EOF handling rule
def t_comments_eof(t):
    if t.lexer.level > 0:  # guardar este error y actuar acorde
        print("Comments can not cross file boundaries")
    return None


# Rules for initial state (default state)
def t_id(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(
        t.value, "id"
    )  # Check for reserved words. If it isn't a reserved word is categorized as identifier
    return t


# matching int numbers
def t_int(t):
    r"\d+"
    t.value = int(t.value)
    # r'\d+(\.\d*)?' float numbers
    # t.value = float(t.value)
    return t


def t_comment1(t):
    r"\--.*"
    pass
    # No return value. Token discarded


def t_string(t):
    r"\""
    string_list = []
    # string_to_append = ''
    text = t.lexer.lexdata
    initial = t.lexer.lexpos
    index = t.lexer.lexpos
    final = len(text)

    while index < final and text[index] != '"':
        if text[index] == "\\":
            if text[index + 1] in ["t", "b", "f", "n"]:
                # string_to_append+=f'\\{text[index + 1]}'
                string_list.append(text[index : index + 2])  # \t,\b,\f
            elif text[index + 1] == "\n":  # non scape \n whith \ before
                # string_to_append+='\n'
                string_list.append("\n")
            elif text[index + 1] == "0":  # null character \0 is not allowed
                print("Illegal character \\0 inside string")  # do something about it
            else:
                string_list.append(
                    text[index : index + 2]
                )  # ]character c: take the character in \c
                # string_to_append += text[index + 1]
            index += 2

        elif text[index] == "\n":  # \n whithout and extra \ is not allowed
            print("Illegal character \\n inside string")  # do something about it
            index += 1
        else:
            string_list.append(text[index])
            # string_to_append += text[index + 1]
            index += 1

    if index == final:
        print("String may not cross file boundaries")  # do something about it
    else:
        index += 1

    t.value = "".join(string_list)
    t.type = "string"
    t.lexer.lexpos += index - initial
    t.lexer.lineno += text[initial : index + 1].count("\n")
    # print(t.value)
    # print(string_to_append)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_larrow = r"<-"
t_rarrow = r"=>"
t_lessequal = r"<="


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
