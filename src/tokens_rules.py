# https://www.dabeaz.com/ply/ply.html
# file for PLY rules
# import ply.lex as lex

# Declare the state
states = (
   ('comments','exclusive'),
)


# All lexers must provide a list tokens that defines all of the possible token names
# that can be produced by the lexer.
first_tokens = [
    'SEMI',
    'COLON',
    'COMMA',
    'DOT',
    'OPAR',
    'CPAR',
    'OCUR',
    'CCUR',
    'AT',
    'LARROW',
    'RARROW',
    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'LESS',
    'EQUAL',
    'LESSEQUAL',
    'NEG',
    'ID',
    'NUM',
    'STRING',
]

reserved = {
    'class':'CLASS',
    'inherits':'INHERITS',
    'not':'NOT',
    'isvoid':'ISVOID',
    'let':'LET',
    'in':'IN',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'fi':'FI',
    'loop':'LOOP',
    'pool':'POOL',
    'case':'CASE',
    'of':'OF',
    'esac':'ESAC',
    'while' : 'WHILE',
    'new' : 'NEW',
    'true' : 'TRUE',
    'false' : 'FALSE'
}
 
tokens = first_tokens + list(reserved.values())

# Match the first (*. Enter comments state.
def t_comments(t):
    r'\(\*'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial level
    t.lexer.begin('comments')                     # Enter 'comments' state

# # Match the first ". Enter strings state.
# def t_strings(t):
#     r'"'
#     t.lexer.code_start = t.lexer.lexpos        # Record the starting position
#     t.lexer.string_list = []
#     t.lexer.begin('strings')                     # Enter 'strings' state

# Rules for the strings state
# def t_strings_startsymb(t):     
#     r'\"'
#     t.lexer.level +=1                

# def t_strings_endsymb(t):
#     r'"'
#     # t.value = t.lexer.string_list
#     t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos - 1]
#     t.type = "STRING"
#     t.lexer.lineno = t.value.count('\n')
#     # t.lexer.lineno += t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1].count('\n')
#     t.lexer.begin('INITIAL')
#     return t

# # def t_comments_anything(t):
# #     r'(?!\(\*|\*\))'   

# # For bad characters, we just skip over it
# def t_strings_error(t):
#     t.lexer.skip(1)
    
# # EOF handling rule
# def t_strings_eof(t):
#     if t.lexer.level > 0:#guardar este error y actuar acorde
#         print("Strings can not contain EOF caracter nor cross file boundaries")
#     return None

# Rules for the comments state
# Comments starting symbol
def t_comments_opsymb(t):     
    r'\(\*'
    t.lexer.level +=1                

# Comments closing symbol
def t_comments_clsymb(t):
    r'\*\)'
    t.lexer.level -=1

    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')


# For bad characters. In this case we just skip over everything but (* or *)
def t_comments_error(t):
    t.lexer.skip(1)
    
# EOF handling rule
def t_comments_eof(t):
    if t.lexer.level > 0:#guardar este error y actuar acorde
        print("Comments can not cross file boundaries")
    return None
    
# Rules for initial state (default state)
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')    # Check for reserved words. If it isn't a reserved word is categorized as identifier
     return t

#matching int numbers
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    # r'\d+(\.\d*)?' float numbers
    # t.value = float(t.value)    
    return t

def t_COMMENT1(t):
    r'\--.*'
    pass
    # No return value. Token discarded


def t_STRING(t):
    # r'\"[^\"]*\"'
    r'\"'
    string_list = []
    # string_to_append = ''
    text = t.lexer.lexdata
    initial = t.lexer.lexpos
    index = t.lexer.lexpos
    final = len(text)

    while(index < final and text[index]!= '"'):
        if(text[index] == '\\'):
            if(text[index + 1] in ['t','b','f','n']):
                # string_to_append+=f'\\{text[index + 1]}'
                string_list.append(text[index:index + 2])#\t,\b,\f
            elif(text[index + 1] == '\n'):#non scape \n whith \ before
                # string_to_append+='\n'
                string_list.append('\n')
            elif(text[index + 1] == '0'):#null character \0 is not allowed
                print("Illegal character \\0 inside string")#do something about it
            else:
                string_list.append(text[index:index + 2])#]character c: take the character in \c
                # string_to_append += text[index + 1]
            index += 2
        
        elif(text[index] == '\n'):#\n whithout and extra \ is not allowed
            print("Illegal character \\n inside string")#do something about it
            index += 1
        else:
            string_list.append(text[index])
            # string_to_append += text[index + 1]
            index += 1

    if(index == final):
        print("String may not cross file boundaries")#do something about it
    else:
        index+=1

    t.value =  ''.join(string_list)
    t.type = 'STRING'
    t.lexer.lexpos += index - initial
    t.lexer.lineno += text[initial:index+1].count('\n')
    # print(t.value)
    # print(string_to_append)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

 
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_OPAR  = r'\('
t_CPAR  = r'\)'
t_OCUR  = r'\{'
t_CCUR  = r'\}'
t_AT = r'\@'
t_LARROW = r'<-'
t_RARROW = r'=>'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_STAR   = r'\*'
t_DIV  = r'/'
t_LESS = r'<'
t_EQUAL = r'='
t_LESSEQUAL = r'<='
t_NEG = r'~'


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 

 # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


