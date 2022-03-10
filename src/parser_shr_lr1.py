from dataclasses import dataclass
from typing import  Any, Dict
from enum import Enum, auto
from generated_utils.automaton_class import Automaton, State
from generated_utils.grammar_classes import Item, Terminal, Epsilon
from generated_utils.serializer_class import Serializer
from generated_utils.token_class import Token

@dataclass
class ParserSymbol:
    name: Any
    tag: Any = None

class ParserTable(Serializer):
    class Action(Enum): 
        SHIFT = auto()
        REDUCE = auto()
        OK = auto()

    def __init__(self):
        self.start_symbol = None
        self.start_state = None
        self.dict_action: Dict[(Any, str), (ParserTable.Action, Any)] = dict()
        self.dict_goto: Dict[(Any, str), Any] = dict()

    def action(self, key, value=None):
        if value is None:
            return self.dict_action.get(key, (None, None))
        if key in self.dict_action and not self.dict_action[key]== value:
            raise ValueError(f"Conflict Occured")
        self.dict_action[key] = value

    def goto(self, key, value=None):
        if value is None:
            return self.dict_goto[key]
        self.dict_goto[key] = value

def parser_shr(tokens_list,ast_class,table:ParserTable,attr_decoder):
        state_stack = [table.start_state]
        symbol_stack = []
        cursor = 0
        while True:
            token:Token=tokens_list[cursor]
            state = state_stack[-1]
            action, tag = table.action((state, token))
            if action==table.Action.SHIFT:
                state_stack.append(tag)
                symbol = ParserSymbol(token.id,token)
                symbol_stack.append(symbol)
                cursor += 1
            elif action ==table.Action.REDUCE:
                to_remov_state=len(state_stack)-tag[1]    
                state_stack=state_stack[:to_remov_state]
                n_last_state=state_stack[-1]
                to_remov_symbol=len(symbol_stack)-tag[1]    
                s_to_reduce= symbol_stack[to_remov_symbol:]
                symbol_stack = symbol_stack[:to_remov_symbol]
                reduced=attr_decoder(tag[2],s_to_reduce,ast_class)
                symbol_stack.append(ParserSymbol(tag[0],reduced))
                state_stack.append(table.goto((n_last_state,tag[0])))
            elif action ==table.Action.OK:
                s=symbol_stack.pop()
                return s.tag,[]
            else:
                col_error=0 if token.lexeme=='$' else token.col_no
                line_error=0 if len(tokens_list)==1 else token.line_no
                return None,[f'({line_error}, {col_error}) - SyntacticError: ERROR at or near "{token.lexeme}"']    

def parser_lr1(grammar):
        table = ParserTable()
        table.start_symbol = grammar.start_symbol.name
        S = grammar.nonTerminals(f"{repr(grammar.start_symbol)}*")
        S != grammar.start_symbol
        grammar.start_symbol = S

        start_value = [Item(next(iter(grammar.start_symbol.productions)), 0, [grammar.eof])]
        automaton=Automaton.to_deterministic(start_value,grammar.goto_lr1,grammar.clousure_lr1,grammar.state_constr,grammar.vocabulary)
        print(f"automaton states {len(automaton.states)}")
        table.start_state = automaton.start.name
        states=automaton.states
        c_is_reduce=0
        for state in states:
            state:State
            for item in state.tag:
                if item.is_reduce:
                    c_is_reduce+=1
                    if item.production.left == grammar.start_symbol:
                        key = (state.name, grammar.eof.name)
                        value = (table.Action.OK, 0)
                        table.action(key,value)    
                    else:
                        for lookahead in item.lookaheads:
                            key = (state.name, lookahead.name)
                            attr=grammar.attr_encoder(item.production.attr)
                            right_s_count=0
                            if not isinstance(item.production.right.symbols[0],Epsilon):
                                right_s_count=len(item.production.right.symbols)
                            value = (table.Action.REDUCE, (item.production.left.name,right_s_count,attr))
                            table.action(key,value)
                else:
                    symbol=item.next_symbol
                    key = (state.name, symbol.name)
                    if isinstance(symbol,Terminal):
                        l=state[symbol.name]
                        value =(table.Action.SHIFT, l.name)
                        table.action(key,value)
                    else:
                        value = state[symbol.name].name
                        table.goto(key, value)
        print(f"action_count:{len(table.dict_action)}")
        keys=list(table.dict_action.values())
        s=0
        r=0
        for c in keys:
            if c[0]==table.Action.REDUCE:r+=1
            if c[0]==table.Action.SHIFT:s+=1
        print(f"action_shift:{s}")
        print(f"action_reduce:{r}") 
        print(f"goto:{len(table.dict_goto)}")                
        return table
