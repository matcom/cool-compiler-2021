from typing import Iterable, List

class Symbol:
    def __init__(self, name:str):
        self.name:str = name

    def __str__(self)->str:
        return self.name

    def __repr__(self):
        return repr(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __len__(self):
        return 1

    def __truediv__(self, other):
        if not isinstance(other, Symbol):
            return AttrSentence(Sentence(self), other)
        else:
            raise TypeError(f"Invalid type: {type(other)}")
    
    def __add__(self, other)->"Sentence":
        if isinstance(other, Symbol):
            return Sentence(self, other)
        if isinstance(other,AttrSentence):
            return AttrSentence(Sentence(self)+other.sentence,other.attr)    
        raise TypeError(f"Invalid type: {other}")

    def __or__(self, other)->"OrSentence":
        if isinstance(other,Symbol):    
            return OrSentence(Sentence(self), Sentence(other))
        if isinstance(other, (Sentence)) or isinstance(other,(AttrSentence)):
            return OrSentence(Sentence(self), other)
        raise TypeError(f"Invalid type: {other}")

    
class Terminal(Symbol):
    def __init__(self, name:str, matcher:str, type=None):
        super().__init__(name)
        self.matcher:str=matcher
        self.type=type
    

class AttrSentence:
    def __init__(self, sentence:"Sentence", attr):
        self.sentence: Sentence = sentence
        self.attr = attr

    def __str__(self) -> str:
        return f"{self.sentence} / {self.attr}"    

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self)

    def __eq__(self, other) -> bool:
        return hash(self)==hash(other)

    def __or__(self, other):
        if isinstance(other, Symbol):
            return OrSentence(self, Sentence(other))
        if isinstance(other, Sentence) or isinstance(other, AttrSentence):
            return OrSentence(self,other)
        raise TypeError(f"Invalid type: {type(other)}")


class Sentence:
    def __init__(self, *args:Symbol):
        self.symbols=(args[0],) if len(args)==1 else  tuple(x for x in args if not isinstance(x,Epsilon))

    def __repr__(self):
        x=" ".join(map(repr,self.symbols))
        return x

    def __hash__(self) -> int:
        return hash(self.symbols)

    def __eq__(self,other)->bool:
        return hash(self)==hash(other)

    def __len__(self)->int:
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def __getitem__(self, index):
        return self.symbols[index]

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(*(self.symbols + (other,)))
        if isinstance(other, Sentence):
            return Sentence(*(self.symbols + other.symbols))
        if isinstance(other,AttrSentence):
            return AttrSentence(self+other.sentence,other.attr)    
        raise TypeError(f"Invalid type: {type(other)}")

    def __or__(self, other):
        if isinstance(other, Symbol):
            return OrSentence(self, Sentence(other))
        if isinstance(other, Sentence) or isinstance(other,AttrSentence):
            return OrSentence(self, other)
        raise TypeError(f"Invalid type: {type(other)}")


class OrSentence:
    def __init__(self,*args):
        self.sentences=list(args)
    
    def __repr__(self):
        rep= [f"| {x}" for x in self.sentences]
        return rep
        
    def __iter__(self):
        return iter(self.sentences)

    def __or__(self, other):
        if isinstance(other, Symbol):
            self.sentences.append(Sentence(other))
        elif isinstance(other, Sentence) or isinstance(other, AttrSentence):
            self.sentences.append(other)
        else:    
            raise TypeError(f"Invalid type: {type(other)}")
        return self    


class Epsilon(Terminal):
    def __init__(self):
        super().__init__("€", "")

    def __str__(self):
        return "€"

    def __repr__(self):
        return "€"


class EOF(Terminal):
    def __init__(self):
        super().__init__("$", "")

    def __str__(self) -> str:
        return "$"

    def __repr__(self):
        return "$"    


class NonTerminal(Symbol):
    def __init__(self, name:str, grammar):
        super().__init__(name)
        self.grammar=grammar
        self.productions:List[Production]=[]

    def __ne__(self, other):
        if isinstance(other,Symbol):
            production=Production(self,Sentence(other))
        
        elif isinstance(other,AttrSentence):
            production=Production(self,other.sentence,other.attr)
            
        elif isinstance(other, Sentence):
            production = Production(self, other)    

        elif isinstance(other, OrSentence):
            for s in other.sentences:
                self.__ne__(s)
            return 
        
        else:
            raise TypeError(f"Invalid type: {type(other)}")
        
        if self.grammar.start_symbol is None:
            self.grammar.start_symbol = self

        if production.attr and production in self.grammar.productions:
            raise ValueError(f"Production {production} was already in the grammar")

        self.productions.append(production)
        self.grammar.productions.append(production)


class Production:
    def __init__(self, non_terminal:NonTerminal, sentence:Sentence,attr=None):
        self.left:NonTerminal= non_terminal
        self.right:Sentence = sentence
        self.attr=attr

    def __str__(self):
        attr_rep=self.attr if self.attr else ""
        return f"{self.left} != {self.right} {attr_rep} "

    def __repr__(self):
        attr_rep=self.attr if self.attr else ""
        return f"{self.left} != {self.right} {attr_rep} "

    def __hash__(self):
        return hash((self.left, self.right))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __iter__(self):
        yield self.left
        yield self.right
    

class Item:
    def __init__(self, production: Production, pos: int = 0, lookaheads: Iterable[Symbol] = None):
        self.production = production
        self.pos = pos
        if isinstance(self.production.right[0],Epsilon): self.pos+=1 #reduce
        if lookaheads: self.lookaheads=tuple(sorted(set(lookaheads),key=hash))
        else: self.lookaheads=tuple()

    def __str__(self):
        item_right = " ".join(map(repr, self.production.right[:self.pos])) + "."
        item_right += " ".join(map(repr, self.production.right[self.pos:])) + ", "
        item_right += "/".join(map(repr, self.lookaheads))
        return f'{self.production.left} -> {item_right}'
        
    def __repr__(self):
        item_right = " ".join(map(repr, self.production.right[:self.pos])) + "."
        item_right += " ".join(map(repr, self.production.right[self.pos:])) + ", "
        item_right += "/".join(map(repr, self.lookaheads))
        return f'{self.production.left} -> {item_right}'

    def __hash__(self):
        return hash((self.production, self.pos, tuple(self.lookaheads)))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    @property
    def is_reduce(self):
        return self.pos == len(self.production.right)

    @property
    def next_symbol(self):
        if not self.is_reduce:
            return self.production.right[self.pos]

    @property
    def next_item(self):
        if not self.is_reduce:
            return Item(self.production, self.pos + 1, self.lookaheads)    

    @property
    def center(self):
        return Item(self.production,self.pos)

    @property
    def preview(self):
        p = self.production.right[self.pos + 1:]
        return [Sentence(*(p + (lookahead,))) for lookahead in self.lookaheads]
