from collections import deque
from typing import List,Dict,Iterable
from itertools import chain
import inspect
import os.path

from lexer_base import *
from parser_base import Parser
from parsers import parser_lr1
from automaton_class import *
from state_class import *
from grammar_classes import *



class Grammar:
    def __init__(self,name:str,attr_decoder=None):
        if attr_decoder:
            self.attr_decoder=attr_decoder
        self.name:str=name
        self.start_symbol: NonTerminal | None = None
        self.eof: EOF = EOF()
        self.epsilon: Epsilon = Epsilon()
        self.terminals: List[Terminal | EOF] = [self.eof, self.epsilon]
        self.non_terminals: List[NonTerminal] = []
        self.productions: List[Production] = list()
        self.firsts: Dict[Sentence, set[Terminal]] | None = None

    # NonTerminal(name, grammar)
    def nonTerminals(self, *names):
        n_t_c=len(names)
        temp=[]
        for name in names:
            n_t=NonTerminal(name, self)
            self.non_terminals.append(n_t)
            temp.append(n_t)
        return temp[0] if n_t_c==1 else temp

    #Terminal(name, match)
    def terminal(self, *ids_match):
        t_c=len(ids_match)
        temp=[]
        for tok in ids_match:
            id,lexeme=tok[0],tok[1]
            type=tok[2] if len(tok)>2 else None
            t=Terminal(id,lexeme,type)
            self.terminals.append(t)
            temp.append(t)
        return temp[0] if t_c==1 else temp

    def compute_local_first(self,sent):
            first_sent = set()
            for fst,snd in enumerate(sent.symbols):
                snd_sent = Sentence(snd)
                fst_snd = self.firsts[snd_sent]
                first_sent.update(fst_snd)
                if self.epsilon not in fst_snd:
                    break
                if fst != len(sent) - 1:
                    first_sent.remove(self.epsilon)
            return first_sent

    def compute_firsts(self, item: "Sentence" = None, accepts_eps=True) -> set[Terminal]:
        if self.firsts is None:
            self.firsts = {Sentence(s): ({s} if isinstance(s, Terminal) else set()) for s in
                                   chain(self.terminals, self.non_terminals)}
            change = True
            while change:
                change= False
                for production in self.productions:
                    right=production.right
                    left=production.left
                    left_s=Sentence(left)
                    local_first = self.compute_local_first(right)
                    change |= right not in self.firsts or len(local_first - self.firsts[right]) != 0
                    change |= len(local_first - self.firsts[left_s]) != 0 
                    self.firsts[left_s].update(local_first)
                    self.firsts[right] = self.firsts.get(right, local_first) | local_first

        res = self.compute_local_first(item)
        return res if accepts_eps else res - {self.epsilon}

    def goto_lr1(self, items: Iterable[Item], symbol: Symbol):
        goto=set()
        for item in items:
            if item.next_symbol==symbol:
                goto.add(item.next_item)
        return tuple(sorted(goto,key=hash))   

    def clousure_lr1(self, items: Iterable[Item]):
        closure = deque(items)
        lr0_dict: Dict[Item, Item] = {}
        for i in items:
            lr0_dict[i.center]=i
        
        while closure:
            current = closure.popleft()
            ## EXPAND
            current_nxt_s = current.next_symbol
            if isinstance(current_nxt_s, NonTerminal):
                lookaheads = set()

                for preview in current.preview:
                    lookaheads.update(self.compute_firsts(preview, accepts_eps=False))

                for prod in current_nxt_s.productions:
                    lr0_item = Item(prod)
                    item=lr0_dict.get(lr0_item, None)
                    if item: #adding new loookaheads
                        item.lookaheads = tuple(sorted(set(chain(item.lookaheads, lookaheads)),key=hash))
                    else:
                        item = Item(prod, 0, lookaheads)
                        lr0_dict[lr0_item] = item
                        closure.append(item)
        return tuple(lr0_dict.values())

    def state_constr(self,tag):
        return State(None,True,tag)

    def vocabulary(self,items):
        res=set()
        for item in items:
            item:Item
            n_s=item.next_symbol
            if n_s:res.add(n_s)
        return sorted(res,key=hash)    

    @staticmethod #/ (class,(positions))
    def attr_encoder(attr):
        if attr:
            if len(attr) == 2:
                attr_name = attr[0].__name__
                attr_pos = attr[1]
                return attr_name, attr_pos
            if isinstance(attr[0], int):
                return (attr[0],)
            if isinstance(attr[0], type):
                return (attr[0].__name__,)
            raise Exception("Invalid Attribute")
        return None

    def attr_decoder(attr, symbols_to_reduce, ast_class):
        if attr:
            if len(attr)==2:
                attr_class, attr_pos = attr
                args = list(map(lambda i: symbols_to_reduce[i].tag, attr_pos))
                return getattr(ast_class, attr_class)(*args)
            if len(attr) == 1:
                if isinstance(attr[0], int):
                    attr_pos = attr[0]
                    return symbols_to_reduce[attr_pos].tag
                elif isinstance(attr[0], str):
                    attr_class = attr[0]
                    arg = symbols_to_reduce[0].tag if len(symbols_to_reduce) else None
                    return getattr(ast_class, attr_class)(arg)
                else:
                    raise Exception("Invalid Attribute")
            else:
                raise Exception("Invalid Attribute")
        return symbols_to_reduce[0].tag if len(symbols_to_reduce) else None

    def lexer(self, path,ignore=" ",eof="$",eoline="\n"):
        lexer_ser=LexerTable(ignore=ignore, eof=eof, eoline=eoline)
        for t in filter(lambda s: not (isinstance(s, Epsilon) or isinstance(s, EOF)), self.terminals):#making match table
            lexer_ser.append((t.name, t.matcher,t.type))
        serialized = lexer_ser.serializer()
        lexer_file = inspect.getfile(Lexer)
        lexer_content = open(lexer_file).read().replace("--LEXER--",serialized)
        this_path = os.path.join(path, f"lexer_{self.name}.py")
        new_path = open(this_path, "w")
        new_path.write(lexer_content)
        new_path.close()

    def parser(self, path= None):
        table=parser_lr1(self)
        serialized = table.serializer()
        parser_file = inspect.getfile(Parser)
        parser_content = open(parser_file).read()
        a_d = inspect.getsource(self.attr_decoder)
        a_d_r = inspect.cleandoc(a_d).replace("\n", "\n" + " " * 4)
        code = parser_content.replace("def attr_decoder(self,attr, symbols_to_reduce, ast_class): pass", a_d_r)
        parser_content = code.replace("--PARSER--", serialized)
        this_path = os.path.join(path, f"parser_{self.name}.py")
        new_path = open(this_path, "w")
        new_path.write(parser_content)
        new_path.close()

