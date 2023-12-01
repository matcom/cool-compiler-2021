from utils.parser.shift_reduce_parser import ShiftReduceParser
from cmp.automata import State, multiline_formatter
from cmp.utils import ContainerSet
from cmp.pycompiler import Item

class LR1_Parser(ShiftReduceParser):
    
    def _build_parsing_table(self):
        
        automaton = self.build_automaton(self.G)
        self.automaton = automaton

        for i, node in enumerate(automaton):
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:

                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                p = item.production
                if item.IsReduceItem:
                    if p.Left == self.G.startSymbol:
                        self._register(self.action,(idx,self.G.EOF.Name),(ShiftReduceParser.OK,None))
                    else:
                        for c in item.lookaheads:
                            self._register(self.action,(idx,c.Name),(ShiftReduceParser.REDUCE,self.G.Productions.index(p)))
                else:
                    
                    if item.NextSymbol.IsTerminal:
                        self._register(self.action,(idx,item.NextSymbol.Name),(ShiftReduceParser.SHIFT, node[item.NextSymbol.Name][0].idx))
                    else:
                        self._register(self.goto,(idx,item.NextSymbol.Name),(node[item.NextSymbol.Name][0].idx))
   

    def build_automaton(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
        
        firsts = self.firsts
        firsts[G.EOF] = ContainerSet(G.EOF)
        
        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0, lookaheads=(G.EOF,))
        start = frozenset([start_item])
        
        closure = self.closure_lr1(start, firsts)
        automaton = State(frozenset(closure), True)
        
        pending = [ start ]
        visited = { start: automaton }
        
        while pending:
            current = pending.pop()
            current_state = visited[current]
            
            for symbol in G.terminals + G.nonTerminals:
                #  (Get/Build `next_state`)
                a = self.goto_lr1(current_state.state,symbol,firsts,True)
                
                if not a:
                    continue
                    
                try:
                    next_state = visited[a]
                except:
                    next_state = State(frozenset(self.goto_lr1(current_state.state,symbol,firsts)),True)
                    visited[a] = next_state
                    pending.append(a)
                
                current_state.add_transition(symbol.Name, next_state)
        
        automaton.set_formatter(multiline_formatter)
        return automaton
    

    def goto_lr1(self,items, symbol, firsts=None, just_kernel=False):
        assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
        items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
        return items if just_kernel else self.closure_lr1(items, firsts)


    def closure_lr1(self,items, firsts):
        closure = ContainerSet(*items)
        
        changed = True
        while changed:
            changed = False
            
            new_items = ContainerSet()

            #por cada item hacer expand y añadirlo a new_items
            for item in closure:
                e = self.expand(item,firsts)
                new_items.extend(e)

            changed = closure.update(new_items)
            
        return self.compress(closure)


    def compress(self,items):
        centers = {}

        for item in items:
            center = item.Center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.lookaheads)
        
        return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }
    

    def expand(self,item, firsts):
        next_symbol = item.NextSymbol
        if next_symbol is None or not next_symbol.IsNonTerminal:
            return []
        
        lookaheads = ContainerSet()
        #  (Compute lookahead for child items)
        #calcular el first a todos los preview posibles
        for p in item.Preview():
            for first in self.compute_local_first(firsts,p):
                lookaheads.add(first)
        
        assert not lookaheads.contains_epsilon
        #  (Build and return child items)
        _list = []
        for production in next_symbol.productions:
            _list.append(Item(production,0,lookaheads))
        return _list

    def __str__(self):
        return 'LR(1)'