from utils.parser.LR_1 import LR1_Parser
from cmp.automata import State, multiline_formatter
from cmp.utils import ContainerSet
from cmp.pycompiler import Item

class LALR1_Parser(LR1_Parser):
    
    def build_automaton(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented' 
    
        firsts = self.firsts
        firsts[G.EOF] = ContainerSet(G.EOF)
    
        start_production = G.startSymbol.productions[0] 
        start_item = Item(start_production, 0, lookaheads=ContainerSet(G.EOF)) 
        start = frozenset([start_item.Center()]) 
    
        closure = self.closure_lr1([start_item], firsts) 
        automaton = State(frozenset(closure), True) 
    
        pending = [start] 
        visited = {start: automaton} 
    
        while pending: 
            current = pending.pop() 
            current_state = visited[current] 
    
            for symbol in G.terminals + G.nonTerminals: 
                a = self.goto_lr1(current_state.state, symbol, just_kernel=True) 
                closure = self.closure_lr1(a, firsts) 
                center = frozenset(item.Center() for item in a)
    
                if not a:
                    continue 
    
                try: 
                    next_state = visited[center] 
                    centers = {item.Center(): item for item in next_state.state} 
                    centers = {item.Center(): (centers[item.Center()], item) for item in closure} 
    
                    updated_items = set() 
                    for c, (itemA, itemB) in centers.items(): 
                        item = Item(c.production, c.pos, itemA.lookaheads | itemB.lookaheads) 
                        updated_items.add(item) 
    
                    updated_items = frozenset(updated_items) 
                    if next_state.state != updated_items: 
                        pending.append(center) 
                    next_state.state = updated_items 

                except KeyError: 
                    visited[center] = next_state = State(frozenset(closure), True) 
                    pending.append(center) 
    
                if current_state[symbol.Name] is None: 
                    current_state.add_transition(symbol.Name, next_state) 
                else: 
                    assert current_state.get(symbol.Name) is next_state, 'Error!!!' 
    
        automaton.set_formatter(multiline_formatter) 
        return automaton 

    def __str__(self):
        return 'LALR(1)'