from enum import Enum, auto
from generated_utils.automaton_class import Automaton,State
from generated_utils.token_class import Token
from typing import Union
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain

INVALID = {"", ""}
SPECIAL = {"”","“","∗","\0","≤"}
ALPHABET = set(chain.from_iterable([string.printable,SPECIAL])) - INVALID
DIGIT = set(iter(string.digits))
NONDIGIT = ALPHABET - DIGIT

def any_escaper(left: Union[Token ,None], right: Union[Token,None]):
    if left.lexeme == "." and right.lexeme == "." or left.lexeme =="\\" and right.lexeme != ".":
        lex = right.lexeme
        res= DIGIT if lex=="d" else NONDIGIT if lex=="D" else ALPHABET if lex=="." else lex
        return res
    return {right.lexeme}


def transitions_appender(chars):
    res = Automaton()
    state = State()
    final = State(final=True)
    res.add_state(state)
    res.add_state(final)
    for char in chars:
        state[char] = final
    return res


class TOKEN_TYPE(Enum):
    ALT = auto()
    STAR = auto()
    PLUS = auto()
    MINUS = auto()
    ASK = auto()
    ESC = auto()
    DOT = auto()
    ACC = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    CHAR=auto()


@dataclass
class Node(ABC):
    @abstractmethod
    def shift(self):
        pass


class BinaryNode(Node, ABC):
    def __init__(self,left:Union[Node,Token], right:Union[Node,Token]):
        self.left:Union[Node,Token]=left
        self.right:Union[Node,Token]=right

    def __str__(self) -> str:
        return f"LEFT: {self.left} \ RIGHT: {self.right}"    


class UnaryNode(Node, ABC):
    def __init__(self,left:Union[Node,Token]):
        self.left=left

    def __str__(self) -> str:
        return f"LEFT: {self.left}"

# A | B
class UnionNode(BinaryNode):
    def __init__(self, left:Union[Node,Token], right: Union[Node,Token]):
        super().__init__(left, right)

    def shift(self):
        left :Automaton= self.left.shift()
        right:Automaton = self.right.shift()
        return left | right

# A + B
class ConcatenationNode(BinaryNode):
    def __init__(self, left: Union[Node,Token], right: Union[Node,Token]):
        super().__init__(left, right)

    def shift(self):
        left :Automaton= self.left.shift()
        right:Automaton = self.right.shift()
        return left + right

#s* 0-many times
class ClousureStarNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        left:Automaton = self.left.shift()
        res = left.upd_stars()
        return res.upd_finals()

#s+ at least one time
class ClousurePlusNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        left: Automaton = self.left.shift()
        left0 = left.copy()
        left1 = left.copy()
        r = left1.upd_stars()
        res = left0 + r
        return res.upd_finals()


#s? 0-1 times
class ClousureMayNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        left:Automaton = self.left.shift()
        return left.upd_stars()

#(c)
class GrouperNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        return self.left.shift()

#[ElemSet]
class SetterNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        rang=self.left.shift()
        return transitions_appender(rang)

#[^ ElemSet]
class NoSetterNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        alphabet = ALPHABET - self.left.shift()
        return transitions_appender(alphabet)

# . or \
class AnyEscaperNode(BinaryNode):
    def __init__(self, left: Union[Node,Token], right: Union[Node,Token]):
        super().__init__(left, right)

    def shift(self):
        return transitions_appender(any_escaper(self.left,self.right))

# May be a . \ or token 
class ElemSetComNode(BinaryNode):
    def __init__(self, left: Union[Node,Token], right: Union[Node,Token]):
        super().__init__(left, right)

    def shift(self):
        left=any_escaper(self.left.left,self.left.right) if isinstance(self.left , AnyEscaperNode) else None
        left={self.left.lexeme} if isinstance(self.left , Token) else left

        right=any_escaper(self.right.left,self.right.right) if isinstance(self.right , AnyEscaperNode) else None
        right={self.right.lexeme} if isinstance(self.right , Token) else right

        f_left = left if left else self.left.shift()
        f_right = right if right else self.right.shift()
        return set(chain(f_left, f_right))

#[a-c] abc
class RangeNode(BinaryNode):
    def __init__(self, left: Union[Node,Token], right: Union[Node,Token]):
        super().__init__(left, right)

    def shift(self):
        left = self.left.lexeme
        right = self.right.lexeme
        if ord(left) > ord(right):
            raise Exception("Invalid Input Range Order")
        
        chars=set()    
        for x in range(ord(left),ord(right)+1):
            chars.add(chr(x))
        return chars

# a Token Char needs to be converted into a automaton to have a way to be shifted 
class CharNode(UnaryNode):
    def __init__(self, left: Union[Node,Token]):
        super().__init__(left)

    def shift(self):
        tag = self.left.lexeme
        return transitions_appender([tag])
