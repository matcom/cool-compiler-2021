from itertools import chain
from typing import Any, Dict, List

class State:
    def __init__(self, name=None, final=False, tag=None):
        self.name: int=name
        self.final: bool = final
        self.tag = tag
        self.transitions: Dict[Any,State]= dict()
        self.epsilon_transitions: List[State] = list()

    def __str__(self):
        return f"{self.name} : {self.tag}"
    
    def __repr__(self):
        return f"{self.name} : {self.tag}"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other:"State"):
        return hash(self)==hash(other)

    def __add__(self,other:"State"):
        final=self.final or other.final
        if self.tag and other.tag:
            tag=self.tag.__class__(chain(self.tag, other.tag))
        else:
            tag=self.tag or other.tag    
        return State(None, final,tag)

    def __radd__(self, other: "State"):
        if other:
            return self+other
        return self.copy(None)    

    def __getitem__(self, symbol):
        if symbol:
            return self.transitions.get(symbol,None)
        return self.epsilon_transitions

    def __setitem__(self, symbol, value):
        if symbol:
            self.transitions[symbol]=value
        else:    
            self.epsilon_transitions.append(value)
    
    def copy(self,n_st_n):
        name=n_st_n
        if n_st_n:
            name=n_st_n+self.name
        return State(name,self.final,self.tag)
   
    def has_transition(self, symbol):
        return (self.transitions.get(symbol,None) is not None)

    def trans_symbols(self):
        return tuple(self.transitions.keys())    