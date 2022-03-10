from abc import ABC, abstractmethod
from typing import Tuple

class Match(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add_matcher(self, sty: Tuple[str, str, str]):
        pass

    @abstractmethod
    def match(self, mathcstr, pos) -> Tuple[str, str, str]:
        pass

class Token:
    def __init__(self,id,line:int,column:int,lexeme:str):
        self.id: str=id
        self.line_no: int=line
        self.col_no: int=column
        self.lexeme: str=lexeme

    def __str__(self):
        return f"({self.line_no},{self.col_no}) :{self.id} - {self.lexeme}"

    def __repr__(self):
        return f"({self.line_no},{self.col_no}) :{self.id} - {self.lexeme}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return hash(self) == hash(other)

def tokenizer(input:str,ignore:str,eof:str,eoline:str,match:Match):
    tokens = []
    errors=[]
    pos = 0
    line = column = 1
    l = len(input)
    while pos < l:
        char = input[pos]
        id, lexeme, consider, matched = match.match(input, pos)
        
        n_pos,n_line,n_column=lines_column_calculator(line,column,pos,lexeme)
        n_errors=no_admited_calculator(lexeme,consider,line,column)
        errors.extend(n_errors)

        if not matched:
            if n_pos==l and len(lexeme): #EOF CASE
                errors.append(f"({n_line}, {n_column}) - LexicographicError: ERROR EOF in {id} ")
            elif not len(lexeme): #No matched character
                errors.append(f"({line}, {column}) - LexicographicError: ERROR in \"{char}\" ")    
            else:# no scaped, null...
                errors.append(f"({n_line}, {n_column}) - LexicographicError: ERROR in \"{lexeme}\" ")
        else:    
            if not consider[0]:
                lexeme= consider[2] if len(consider)==3 else lexeme 
                token= Token(id, line, column, lexeme )
                tokens.append(token)
        pos=n_pos
        line=n_line
        column=n_column    
    eof = Token(eof,line,column, eof)
    tokens.append(eof)
    return tokens,errors

def lines_column_calculator(c_line:int,c_column:int,c_pos:int,lexeme:str):
    if lexeme:
        lines_to_add=lexeme.count('\n')
        after_linebreak=lexeme[::-1].index('\n') if lines_to_add else None
        if after_linebreak is not None:
            n_column=1 if after_linebreak==0 else after_linebreak+1
        else:    
            n_column= len(lexeme)+ c_column
        n_line=lines_to_add+ c_line
        n_pos=c_pos + len(lexeme)
    else:
        n_column=c_column+1
        n_line=c_line
        n_pos=c_pos+1
    return n_pos,n_line,n_column

def no_admited_calculator(lexeme:str,specials,line,column):
    if not len(lexeme) or not len(specials)>1 or not len(specials[1]):return[]
    n_errors=[]
    for x in specials[1]:
        count=lexeme.count(x)
        if count:
            sub=lexeme
            temp_line=line
            temp_column=column
            while len(sub) and count:
                count-=1
                ind=sub.index(x)
                before=sub[:ind]
                sub=sub[ind+1:]
                _,temp_line,temp_column=lines_column_calculator(temp_line,temp_column,0,before)
                n_errors.append(f"({temp_line}, {temp_column}) - LexicographicError: ERROR CONTAIN {x}")
                temp_column+=1
    return n_errors