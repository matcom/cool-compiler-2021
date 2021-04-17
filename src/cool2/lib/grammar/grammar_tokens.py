from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal)
from cmp.ast import Node, AtomicNode, BinaryNode, TernaryNode
from cmp.utils import Token
from lib.lexer.lexer import Lexer,nonzero_digits,digits,min_letters,cap_letters
from lib.lexer.regex import fixed_tokens, EPSILON, regex_automaton


digits_letters = f'{digits}{min_letters}{cap_letters}'
others = f',.^;:<>=-_!^&~/'
separator = '@'
regex_char_separator = '\n'
regex_separator = f'{regex_char_separator}*'

# Lexer that recognise the token defined by the user
lex_token = Lexer([ ####################################################
    # ('term',f'[{digits_letters}]*'),
    # ('regex_ex',f'{separator}[ \\\\\\[\\]\\+\\?\\*\\(\\)\\|\\{EPSILON}{digits_letters}{others}]*'),
    # ('regex_sep',regex_separator),
],'eof')

# num@12w09djqdk\nlet@[asdcsac]  ==>  num - regex(12w09djqdk)   let - regex([asdcasac])

def get_lexer_from_text(text,errors:list):
    """
    Returns a Lexer that recognise tokens of the form  <term>@<regex>\\n<term>@<regex>\\n...<term>@<regex>\\n\n
    where term is the name of the terminal and regex is the regular expression of term\n
    the order in text is the same that the order of the lexer table
    """
    tokens = lex_token(text)
    lexer_table = []
    tok_iter = iter(tokens)
    new_errors = []
    while True:
        try:
            terminal = next(tok_iter)
        except StopIteration:
            new_errors.append(f'Expected: token')
            break
        
        if terminal.token_type == 'eof':
            break
        
        if not terminal.token_type == 'term':
            new_errors.append(f'Expected: {terminal.lex}.token_type == term, Recieve: {terminal.lex}.token_type == {terminal.token_type}')
            break
        
        try:
            regex = next(tok_iter)
        except StopIteration:
            new_errors.append(f'Expected: token')
            break
        
        if not regex.token_type == 'regex_ex':
            new_errors.append(f'Expected: {regex.lex}.token_type == regex_ex, Recieve: {terminal.lex}.token_type == {terminal.token_type}')
            break
        
        try:
            sep = next(tok_iter)
        except StopIteration:
            new_errors.append(f'Expected: token')
            break
        
        if not (sep.token_type == 'regex_sep' or sep.token_type == 'eof'):
            new_errors.append(f'Expected: {sep.lex}.token_type == regex_sep or eof, Recieve: {terminal.lex}.token_type == {terminal.token_type}')
            break
        
        lexer_table.append((terminal.lex,regex.lex[1:]))
        
        if sep.token_type == 'eof':
            break
        
    for x in new_errors:
        errors.append(x)
    try:
        next(tok_iter)
        errors.append('tokens left to parse')
        return None
    except StopIteration:
        if new_errors:
            return None
        return Lexer(lexer_table,'eof')

def get_lexer_dict_from_text(text,errors:list):
    """
    Returns a dictionary that recognise tokens of the form  <term>@<regex>\\n<term>@<regex>\\n...<term>@<regex>\\n\n
    where term is the name of the terminal and regex is the regular expression of term\n
    """
    tokens = lex_token(text)
    lexer_table = {}
    tok_iter = iter(tokens)
    new_errors = []
    while True:
        try:
            terminal = next(tok_iter)
        except StopIteration:
            new_errors.append(f'Expected: token')
            break
        
        if terminal.token_type == 'eof':
            break
        
        if not terminal.token_type == 'term':
            new_errors.append(f'Expected: {terminal.lex}.token_type == term, Recieve: {terminal.lex}.token_type == {terminal.token_type}')
            break
        
        try:
            regex = next(tok_iter)
        except StopIteration:
            new_errors.append(f'Expected: token')
            break
        
        if not regex.token_type == 'regex_ex':
            new_errors.append(f'Expected: {regex.lex}.token_type == regex_ex, Recieve: {terminal.lex}.token_type == {terminal.token_type}')
            break
        
        try:
            sep = next(tok_iter)
        except StopIteration:
            new_errors.append(f'Expected: token')
            break
        
        if not (sep.token_type == 'regex_sep' or sep.token_type == 'eof'):
            new_errors.append(f'Expected: {sep.lex}.token_type == regex_sep or eof, Recieve: {terminal.lex}.token_type == {terminal.token_type}')
            break
        
        lexer_table[terminal.lex] = regex_automaton(regex.lex[1:])
        
        if sep.token_type == 'eof':
            break
        
    for x in new_errors:
        errors.append(x)
    try:
        next(tok_iter)
        errors.append('tokens left to parse')
        return None
    except StopIteration:
        if new_errors:
            return None
        return lexer_table
