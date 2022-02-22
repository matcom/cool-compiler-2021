# https://www.dabeaz.com/ply/ply.html
# file for PLY rules

from errors import (
    tokenizer_error,
    LexicographicError,
    UnexpectedCharError,
    UnexpectedEOFError,
    UnexpectedTokenError,
)


# def find_column(input, lexpos):
#     # line_start = input.rfind("\n", 0, lexpos) + 1
#     # return (lexpos - line_start) + 1
#     line_numbers = input.rfind("\n", 0, lexpos) + 1
#     return (lexpos // line_numbers) + (lexpos % line_numbers)


# Declare the states
states = (("comments", "exclusive"),)


# All lexers must provide a list tokens that defines all of the possible token names
# that can be produced by the lexer.
# first_tokens = [
#     "larrow",
#     "rarrow",
#     "lessequal",
#     "id",
#     "int",
#     "string",
# ]
first_tokens = [
    "larrow",
    "rarrow",
    "lessequal",
    "id",
    "int",
    "string",
    "ccom"
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
    # t.lexer.lineno += len(t.value)
    t.lexer.last_new_line_pos = t.lexer.lexpos
    t.lexer.lineno += 1

# t_foo_end(t)
# Comments closing symbol
# def t_comments_clsymb(t):
def t_comments_ccom(t):
    r"\*\)"
    t.lexer.level -= 1

    if t.lexer.level == 0:
        # t.value = t.lexer.lexdata[t.lexer.code_start : t.lexer.lexpos + 1]
        t.value = t.lexer.lexdata[t.lexer.code_start : t.lexer.lexpos -2] # comments should not be returned, just skipped
        t.type = "ccom"
        # t.lexer.lineno += t.value.count("\n")
        # t.lexer.lineno +=1#after the last closing symbol add new line 
        t.lexer.begin("INITIAL")
        return t
        
def t_comments_any(t):
# def t_ccode_nonspace(t):
    r'[^\s\{\}\'\"]+'
    # r'^[^ \n]+$'
    # r"\.*"
    # print("ANY")
    # print(t.lexer.lexdata[t.lexer.lexpos -1])
    # t.lexer.skip(1)

# For bad characters. In this case we just skip over everything but (* or *)
def t_comments_error(t):
    # t.lexer.errors.append(
    #     LexicographicError(
    #         t.lexer.lineno,
    #         0,
    #         "Illegal character inside comment",
    #     )
    # )
    # print("character skipped")
    # print(t.lexer.lexdata[t.lexer.lexpos -1])
    t.lexer.skip(1)


# EOF handling rule
def t_comments_eof(t):
    if t.lexer.level > 0:  # guardar este error y actuar acorde
        # print(f"code_start{t.lexer.code_start}")
        t.lexer.errors.append(LexicographicError(t.lexer.lineno, t.lexer.lexpos - t.lexer.last_new_line_pos, "EOF in comment"))
    return None


# Rules for initial state (default state)
def t_id(t):
    r"[a-zA-Z][a-zA-Z_0-9]*"
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
    r"\" "
    string_list = []
    text = t.lexer.lexdata
    initial = t.lexer.lexpos
    index = t.lexer.lexpos
    final = len(text)
    while index < final and text[index] != '"':
        if text[index] == "\\":
            if text[index + 1] in ["t", "b", "f", "n"]:
                # string_to_append+=f'\\{text[index + 1]}'
                string_list.append(text[index : index + 2])  # \t,\b,\f, \n
            elif text[index + 1] == "\n":  # \n whith \ before
                # string_to_append+='\n'
                t.lexer.lineno +=1
                t.lexer.last_new_line_pos = index + 1# saving last \n
                string_list.append("\n")
            elif text[index + 1] == "0":  # null character \0 is not allowed
                # print("Illegal character \\0 inside string")  # do something about it
                # t.lexer.errors.append(
                #     LexicographicError(
                #         t.lexer.lineno + text[initial : index + 1].count("\n"),
                #         index - t.lexer.last_new_line_pos + 2,
                #         "Illegal character \\0 inside string",
                #     )
                # )
                t.lexer.errors.append(
                    LexicographicError(
                        t.lexer.lineno,
                        index - t.lexer.last_new_line_pos + 1,
                        "Illegal character \\0 inside string",
                    )
                )
                t.lexer.lexpos = index+1
                return t
            else:
                string_list.append(#CHEQUEAR PQ ESTO SE AHCE DOS VECES< COMO TRATAR DIFERENTE EL \n
                    text[index : index + 2]
                )  # ]character c: take the character in \c
                # string_to_append += text[index + 1]
            index += 2

        elif text[index] == "\n":  # non scape \n (whithout and extra \) is not allowed
            # print("Illegal character \\n inside string")  # do something about it
            # t.lexer.errors.append(
            #     LexicographicError(
            #         t.lexer.lineno + text[initial : index + 1].count("\n"),
            #         index - t.lexer.last_new_line_pos + 1,
            #         "Illegal character \\n inside string",
            #     )
            # )
            t.lexer.errors.append(
                LexicographicError(
                    t.lexer.lineno,
                    index - t.lexer.last_new_line_pos,
                    "Illegal character \\n inside string",
                )
            )
            t.lexer.lineno +=1
            t.lexer.last_new_line_pos = index# sabing last \n
            # index += 1
            t.lexer.lexpos = index#new
            return t

        else:
            string_list.append(text[index])
            # string_to_append += text[index + 1]
            index += 1

    if index == final:
        # print("String may not cross file boundaries")  # do something about it
        # t.lexer.errors.append(
        #     LexicographicError(
        #         t.lexer.lineno + text[initial : index + 1].count("\n"),
        #         t.lexer.lexpos - t.lexer.last_new_line_pos + 1,
        #         "String may not cross file boundaries",
        #     )
        # )
        t.lexer.errors.append(
            LexicographicError(
                t.lexer.lineno,
                index - t.lexer.last_new_line_pos,
                "String may not cross file boundaries",
            )
        )
        #AQUI NO HACE FALTA ACTUALIZAR index antes?
        t.lexer.lexpos = index
        return t
    else:
        # index += 1

        t.value = "".join(string_list)
        t.type = "string"
        # t.lexer.lexpos += index - initial #RECIEND BORRADO
        t.lexer.lexpos = index# en index se supone este el " de cerrar los comentarios
        # t.lexer.lineno += text[initial : index + 1].count("\n")
        # print(t.value)
        # print(string_to_append)
        return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n"
    # t.lexer.lineno += len(t.value)
    t.lexer.last_new_line_pos = t.lexer.lexpos
    t.lexer.lineno += 1

t_larrow = r"<-"
t_rarrow = r"=>"
t_lessequal = r"<="

# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
def t_error(t):#for some reason here lexpos is the current character, maybe because it could not be matched
    print("ERROR")
    print(t.lexer.lexpos)
    print(t.lexer.last_new_line_pos)
    print("In lex pos")
    print(t.lexer.lexdata[t.lexer.lexpos])
    print("In last new line pos")
    print(t.lexer.lexdata[t.lexer.last_new_line_pos])
    print(t.lexer.lexdata[t.lexer.last_new_line_pos-1])


    t.lexer.errors.append(
        LexicographicError(
            t.lexer.lineno,
            t.lexer.lexpos - t.lexer.last_new_line_pos + 1,
            f"ERROR {t.value[0]}",
        )
    )
    t.lexer.skip(1)
