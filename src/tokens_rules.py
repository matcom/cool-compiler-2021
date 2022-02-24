# https://www.dabeaz.com/ply/ply.html
# file for PLY rules

from errors import (
    tokenizer_error,
    LexicographicError,
    UnexpectedCharError,
    UnexpectedEOFError,
    UnexpectedTokenError,
)

# Declare the states
states = (("comments", "exclusive"),)


# All lexers must provide a list tokens that defines all of the possible token names
# that can be produced by the lexer.
first_tokens = [
    "larrow",
    "rarrow",
    "lessequal",
    "id",
    "type_id",
    "int",
    "string",
]
# Add "ccom" to test comments
 
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
def t_begin_comments(t):
    r"\(\*"
    t.lexer.code_start = t.lexer.lexpos  # Record the starting position
    t.lexer.level = 1  # Initial level
    t.lexer.begin("comments")  # Enter 'comments' state


# Rules for the comments state
# Comments starting symbol
def t_comments_opsymb(t):
    r"\(\*"
    t.lexer.level += 1

# Define a rule so we can track line numbers
def t_comments_newline(t):
    r"\n"
    t.lexer.last_new_line_pos = t.lexer.lexpos
    t.lexer.lineno += 1

# end comments
def t_comments_ccom(t):
    r"\*\)"
    t.lexer.level -= 1

    if t.lexer.level == 0:
        # t.value = t.lexer.lexdata[t.lexer.code_start : t.lexer.lexpos -2] # comments should not be returned, just skipped
        # t.type = "ccom"
        # return t
        t.lexer.begin("INITIAL")
        
def t_comments_any(t):
    # r'[^\s\{\}\'\"]+'
    r'[^\s\'\"]+'
    # t.lexer.skip(1)

# For bad characters. In this case we just skip over everything but (* or *)
def t_comments_error(t):
    t.lexer.skip(1)


# EOF handling rule
def t_comments_eof(t):
    if t.lexer.level > 0:  # guardar este error y actuar acorde
        t.lexer.errors.append(LexicographicError(t.lexer.lineno, t.lexer.lexpos - t.lexer.last_new_line_pos + 1, "EOF in comment"))
    return None
    # t.lexer.skip(1)


# Rules for initial state (default state)

#Object identifiers
def t_id(t):
    r"[a-z][a-zA-Z_0-9]*"
    t.type = reserved.get(
        t.value.lower(), "id"
    )  # Check for reserved words. If it isn't a reserved word is categorized as identifier
    return t

#Type identifiers
def t_type_id(t):
    r"[A-Z][a-zA-Z_0-9]*"
    value_in_lowercase = t.value.lower()
    if value_in_lowercase != "false" and value_in_lowercase != "true":
        t.type = reserved.get(
            value_in_lowercase, "type_id"
        ) # Check for reserved words. If it isn't a reserved word is categorized as identifier
    else:
        t.type = "type_id"#this may be extra as t.type is already setted as type_id 
    # t.lexpos = t.lexpos - t.lexer.last_new_line_pos + 1
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


def t_string(t):# se va a develve el string vacio cada vez que no se puede matchear el string completo
    r"\" "#xq habria que seguir analizando el string cuando se ha encontrado un caracter null y se ha de parar en otros casos?
    string_list = []
    text = t.lexer.lexdata
    initial = t.lexer.lexpos
    index = t.lexer.lexpos
    final = len(text)
    while index < final and text[index] != '\"':
        if text[index] == '\\':
            if text[index + 1] in ["t", "b", "f", "n"]:
                string_list.append(text[index : index + 2])  # \t,\b,\f, \n
            elif text[index + 1] == '\n':  # \n whith \ before
                t.lexer.lineno +=1
                t.lexer.last_new_line_pos = index + 2# saving last \n
                string_list.append('\n')
            else:
                string_list.append(# ESTO SE AHCE DOS VECES< COMO TRATAR DIFERENTE EL \t por ejempli
                    text[index : index + 2]
                )  # ]character c: take the character in \c
            index += 2

        elif text[index] == '\n':  # non scape \n (whithout and extra \) is not allowed
            t.lexer.errors.append(
                LexicographicError(
                    t.lexer.lineno,
                    index - t.lexer.last_new_line_pos + 1,
                    "Unterminated string constant",
                )
            )
            t.lexer.lineno +=1
            t.lexer.last_new_line_pos = index + 1# saving last \n
            t.lexer.lexpos = index + 1
            return t
        elif text[index] == '\0':  # null character \0 is not allowed 
            t.lexer.errors.append(
                LexicographicError(
                    t.lexer.lineno,
                    index - t.lexer.last_new_line_pos + 1,
                    "String contains null character",
                )
            )
            index += 1
            # return t
        else:
            string_list.append(text[index])
            index += 1

    if index == final: # String may not cross file boundaries 
        t.lexer.errors.append(
            LexicographicError(
                t.lexer.lineno,
                index - t.lexer.last_new_line_pos + 1,
                "EOF in string constant",
            )
        )
        t.lexer.lexpos = index
        return t
    else:
        index += 1#jumping '\"' character (character for closing coments)

        t.value = "".join(string_list)
        t.type = "string"
        t.lexer.lexpos = index
        return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.last_new_line_pos = t.lexer.lexpos
    t.lexer.lineno += 1

t_larrow = r"<-"
t_rarrow = r"=>"
t_lessequal = r"<="

# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
def t_error(t):#At the moment of entering this method lexpos is the current character (instead of the last matched character) because nothing could've been matched
    t.lexer.errors.append(
        LexicographicError(
            t.lexer.lineno,
            t.lexer.lexpos - t.lexer.last_new_line_pos + 1,
            f"ERROR {t.value[0]}",
        )
    )
    t.lexer.skip(1)
