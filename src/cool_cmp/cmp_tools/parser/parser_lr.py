from cmp.automata import State, lr0_formatter, multiline_formatter
from cmp.pycompiler import (EOF, Epsilon, Grammar, Item, NonTerminal,
                            Production, Sentence, SentenceFromIter,
                            SentenceList, Symbol, Terminal)
from cmp_tools.utils.first_follow import (compute_firsts, compute_follows, compute_local_first)
from cmp.utils import ContainerSet, DisjointNode, DisjointSet, Token
from cmp_tools.parser.parser import Parser
from cmp_tools.grammar.grammar_fixer import fix_non_derive_terminal
from cmp_tools.utils.automaton import state_transpose
from cool.errors.errors import SyntacticCoolError, SYNTACTIC_ERROR

######################  LR0 and SLR1  ###########################
def get_state(visited,pending,item):
    if not item in visited.keys():
        new_state = State(item,True)
        pending.append(item)
        visited[item] = new_state
        return new_state
    return visited[item]

def build_LR0_automaton(G:Grammar):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue
        
        current_state = visited[current_item]
        next_symbol = current_item.NextSymbol
        next_item = current_item.NextItem()
        
        #- $(X --> a.cB) ---c---> (X --> ac.B)  con c in V_T
        #- $(X --> a.YB) ---Y---> (X --> aY.B)  con Y in V_N
        next_state = get_state(visited,pending,next_item)
        current_state.add_transition(next_symbol.Name,next_state)
        
        if next_symbol in G.nonTerminals:
            sym_productions = G.symbDict[next_symbol.Name].productions
            #- $(X --> a.YB) ---e---> (Y --> .Z)  con Y in V_N
            for pr in [Item(x,0) for x in sym_productions]:
                trans_state = get_state(visited,pending,pr)
                current_state.add_epsilon_transition(trans_state)

    return automaton.to_deterministic(lr0_formatter)

class ShiftReduceParser(Parser):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    lr_type = None
    errors = None
    automaton = None
    grammar = None
    error_states = None # self.error_states[key]  is the set of posibles values
    eval_errors = []
    
    
    state_dict = {} # state_dic[key] = State with idx==key
    
    def __init__(self, G, automaton_builder, verbose=False):
        self.grammar = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self.errors = []
        self.error_states = {}
        G = G.AugmentedGrammar(True)
        self.automaton = automaton_builder(G)
        self._build_parsing_table(G)
    
    def _build_parsing_table(self, G):
        raise NotImplementedError()
    
    def __call__(self, tokens, errors,finding_conflict = False):
        stack = [ 0 ]
        cursor = 0
        output = []
        tokens = [x for x in tokens]
        while True and cursor < len(tokens):
            state = stack[-1]
            lookahead = tokens[cursor]
            if self.verbose: print(stack, '<---||--->', tokens[cursor:])
                
            # Your code here!!! (Detect error)
            try:
                action = self.action[state, lookahead.token_type]
                if isinstance(action,tuple):
                    action, tag = action
                else:
                    return None if not finding_conflict else (state,lookahead,output)
            except KeyError:
                # errors.append(f'Invalid transition ({state},{lookahead}) doesnt exist expected {[ x[1] for x in self.action if x[0] == state ]}')
                posibles = [x for x in self.action if x[0] == state ]
                arg = f"{lookahead.lex[0]}" if lookahead.is_eof else lookahead.lex[0]
                errors.append(SyntacticCoolError(SYNTACTIC_ERROR, arg, token=lookahead))
                # errors.append(f"Invalid transition near '{lookahead.lex[0]}'. Expected: {', '.join([ str(x[1]) for x in posibles ])}. Line:{lookahead.lex[1] + 1} Column:{lookahead.lex[2] + 1}")
                if len(posibles) == 1 and not lookahead.is_eof:
                    tokens.insert(cursor + 1, Token((str(posibles[0][1]), lookahead.lex[1], lookahead.lex[2]), posibles[0][1]))
                    cursor += 1
                    continue
                return None if not finding_conflict else (state,lookahead,output)
            
            if action == self.SHIFT:
            # Your code here!!! (Shift case)
                stack.append(lookahead.token_type)
                stack.append(tag)
                cursor+=1
            elif action == self.REDUCE:
            # Your code here!!! (Reduce case)
                for i in range(len(tag.Right)):
                    stack.pop()
                    top = stack.pop()
                    if top != tag.Right[-(i+1)]:
                        errors.append(f"Productions reduce doesnt match: {top} != {tag.Right[-(i+1)]}")
                        
                index = self.goto[stack[-1],tag.Left]
                stack.append(tag.Left)
                stack.append(index)
                output.append(tag)
            elif action == self.OK:
            # Your code here!!! (OK case)
                return output if not finding_conflict else (state,lookahead,output)
            # Your code here!!! (Invalid case)
            else:
                errors.append(f"Invalid case: {action}")
                return None if not finding_conflict else (state,lookahead,output)

        if cursor == len(tokens):
            errors.append('EOF token missing')

        else:
            errors.append('No valid derivation tree can be built with the given tokens')
    
    def _register(self, table, key, value):
        if key in table:
            key_value = table[key]
            if type(key_value) == type(set()):
                if value not in key_value:
                    self.errors.append(f'Shift-Reduce or Reduce-Reduce conflict: {key} already on table with values {table[key]} cannot register with value {value}')
                    key_value.add(value)
                    if key in self.error_states:
                        self.error_states[key].add(key)
                    else:
                        self.error_states[key] = set([value,key_value])
            elif key_value != value:
                self.errors.append(f'Shift-Reduce or Reduce-Reduce conflict: {key} already on table with value {table[key]} cannot register with value {value}')
                table[key] = set([value, key_value])
                if key in self.error_states:
                    self.error_states[key].add(key)
                else:
                    self.error_states[key] = set([value,key_value])
        else:
            table[key] = value

    def _evaluate(self, production, right_parse, tokens, inherited_value=None):
        head, body = production
        attributes = production.attributes
        body = list(body)
        body.reverse()
        # Insert your code here ...
        # > synteticed = ...
        synteticed = [None for _ in attributes]
        # > inherited = ...
        inherited = [None]*(len(body)+1)
        # Anything to do with inherited_value?
        inherited[0] = inherited_value

        for i, symbol in zip(range(len(body),0,-1),body) :
            if symbol.IsTerminal:
                if not inherited[i] is None:
                    self.eval_errors.append(f'Terminals cant have inherited values. Terminal:{symbol}; Inherited:{inherited[i]}')
                    break
                # Insert your code here ...
                try:
                    synteticed[i] = next(tokens).lex # como es un terminal se sintetiza como el mismo
                except StopIteration:
                    self.eval_errors.append(f'tokens stopped the iteration')
                    break
            else:
                try:
                    next_production = next(right_parse)
                except StopIteration:
                    self.eval_errors.append(f'right_parse stopped the iteration')
                    break
                if not symbol == next_production.Left:
                    self.eval_errors.append(f'{symbol} doesnt match with {next_production.Left}. Cant expand {symbol}')
                    break
                # Insert your code here ...
                if attributes[i]:
                    inherited[i] = attributes[i](inherited, synteticed)
                synteticed[i] = self._evaluate(next_production, right_parse, tokens, inherited[i])

        # Insert your code here ...
        if attributes[0]:
            synteticed[0] = attributes[0](inherited, synteticed)
        # > return ...
        return synteticed[0]

    def evaluate_parse(self, right_parse, tokens):
        self.eval_errors.clear()
        if not right_parse or not tokens:
            self.eval_errors.append('Empty tokens or Empty right_parse')
            return None

        right_parse = iter(right_parse)
        end = tokens[-1]
        tokens = tokens[:len(tokens)-1]
        tokens.reverse()
        tokens.append(end)
        tokens = iter(tokens)
        result = self._evaluate(next(right_parse), right_parse, tokens)

        if not isinstance(next(tokens).token_type, EOF):
            self.eval_errors.append('Last parsed token doesnt match with EOF')
            return None
        return result
    
    def evaluate(self,tokens,errors:list,return_ast=False,parsed_tokens=None):
        """
        If no errors then returns the evaluated tokens\n
        else fills errors with errors returning None
        """
        parser = self.__call__
        new_errors = []
        if parsed_tokens is None:
            right_parse = parser(tokens,new_errors)
        else:
            right_parse = parsed_tokens
        if not new_errors:
            right_parse.reverse()
            ast = self.evaluate_parse(right_parse, tokens)
            if self.eval_errors:
                for x in self.eval_errors:
                    errors.append(x)
                return None
            if return_ast:
                return ast
            return ast.evaluate()
        else:
            for x in new_errors:
                errors.append(x)
            return None

    def find_conflict(self):
        conflicts = []
        automaton_reverse,state_dict = state_transpose(self.automaton)
        for key,value in self.action.items():
            if type(value) == type(set()):
                conflict_productions = [x[1] for x in value if isinstance(x[1],Production)]
                for production in conflict_productions:
                    conflict_state = state_dict[key[0]][0]
                    conflict_item = find_conflict_item(conflict_state,production)
                    stack = [(conflict_state,conflict_item)]
                    
                    sentence = [ y for y in production.Right ]
                    sentence.reverse()
                    current_state = conflict_state
                    current_item = conflict_item
                    for y in sentence:
                        current_item = Item(current_item.production,current_item.pos-1,current_item.lookaheads)
                        current_state = go_back(current_state,y,current_item,state_dict)
                        stack.append((current_state,current_item))
                    stack.reverse()
                    
                    initial_item = find_initial_item(self.automaton)
                    path = [(self.automaton,initial_item,False)]
                    visited = {(initial_item,self.automaton.idx)}
                    find_path_to(stack[0][0],stack[0][1],self.automaton,initial_item,path,visited) # una lista de tuplas que es (estado en que estoy,item en el que estoy)
                        
                    terminals = items_to_terminals(path[:len(path)-1],stack)
                    conflicts.append(self._generate_error(value,terminals,[x[1] for x in path] + [x[1] for x in stack[1:]],key[0],key[1]))
                    break
                
        return conflicts       
    
    def _generate_error(self,conflict,terminals,items,state,lookahead):
        string = ' '.join(x.Name for x in terminals)
        return f'The string "{string}" is generated by the items {items}, stopping in state {state}, the conflict is because the automaton can do the following actions {conflict} looking at terminal "{lookahead}"'
    
class LR0Parser(ShiftReduceParser):

    def __init__(self,G,verbose=False):
        super().__init__(G,build_LR0_automaton,verbose)
        self.lr_type = 'lr0'
    
    def _build_parsing_table(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
               
        automaton = self.automaton
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                item = state.state
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action,(idx,G.EOF),(self.OK,None))
                    else:
                        for c in G.terminals + [G.EOF]:
                            self._register(self.action, (idx,c),(self.REDUCE,item.production))
                else:
                    next_sym = item.NextSymbol
                    try:
                        next_state = node[next_sym.Name][0]
                        if next_sym.IsNonTerminal:
                            self._register(self.goto,(idx,next_sym),next_state.idx)
                        else:
                            self._register(self.action,(idx,next_sym),(self.SHIFT,next_state.idx))
                    except KeyError:
                        self.errors.append(f'Node: {node} without transition with symbol {next_sym}')
                        return None
 
class SLR1Parser(ShiftReduceParser):

    def __init__(self,G,verbose=False):
        super().__init__(G,build_LR0_automaton,verbose)
        self.lr_type = 'slr1'
    
    def _build_parsing_table(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
        
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton =  self.automaton
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                item = state.state
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action,(idx,G.EOF),(self.OK,None))
                    else:
                        for c in follows[item.production.Left]:
                            self._register(self.action, (idx,c),(self.REDUCE,item.production))
                else:
                    next_sym = item.NextSymbol
                    try:
                        next_state = node[next_sym.Name][0]
                        if next_sym.IsNonTerminal:
                            self._register(self.goto,(idx,next_sym),next_state.idx)
                        else:
                            self._register(self.action,(idx,next_sym),(self.SHIFT,next_state.idx))
                    except KeyError:
                        self.errors.append(f'Node: {node} without transition with symbol {next_sym}')
                        return None
    
           
######################  LR1  ###########################
def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet() # lookahead = que yo quiero ver cuando vaya a reducir
    # Your code here!!! (Compute lookahead for child items)

    for prev in item.Preview():
        lookaheads.update(compute_local_first(firsts,prev))
    
    assert not lookaheads.contains_epsilon

    # Your code here!!! (Build and return child items)
    return [ Item(x,0,lookaheads) for x in next_symbol.productions]

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        # Your code here!!!
        for x in closure:
            new_items.extend(expand(x,firsts))

        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
            # Your code here!!! (Get/Build `next_state`)
            next_state_key = goto_lr1(current_state.state,symbol,just_kernel=True)
            # next_state_key = frozenset([i.NextItem() for i in current_state.state if i.NextSymbol == symbol])
            if not next_state_key:
                continue
            try:
                next_state = visited[next_state_key]
            except KeyError:
                next_state_items = goto_lr1(current_state.state,symbol,firsts)
                next_state = State(frozenset(next_state_items),True)
                pending.append(next_state_key)
                visited[next_state_key] = next_state
            current_state.add_transition(symbol.Name, next_state)

    
    automaton.set_formatter(multiline_formatter)
    return automaton

class LR1Parser(ShiftReduceParser):
    
    def __init__(self,G,verbose=False):
        super().__init__(G,build_LR1_automaton,verbose)
        self.lr_type = 'lr1'
    
    def _build_parsing_table(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
               
        automaton = self.automaton
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action,(idx,G.EOF),(self.OK,None))
                    else:
                        for c in item.lookaheads:
                            self._register(self.action, (idx,c),(self.REDUCE,item.production))
                else:
                    next_sym = item.NextSymbol
                    try:
                        next_state = node[next_sym.Name][0]
                        if next_sym.IsNonTerminal:
                            self._register(self.goto,(idx,next_sym),next_state.idx)
                        else:
                            self._register(self.action,(idx,next_sym),(self.SHIFT,next_state.idx))
                    except KeyError:
                        self.errors.append(f'Node: {node} without transition with symbol {next_sym}')
                        return None
        

######################  LALR1  ###########################
def center_of(items):
    return { item.Center() for item in items }

def build_automaton_from_ds(initial:State, ds:DisjointSet):
    for g in ds.groups:
        r = g[0].representative.value
        old_transitions = r.transitions
        r.transitions = {}
        for x in old_transitions:
            node = None
            for y in ds.groups:
                if center_of(y[0].representative.value.state) == center_of(old_transitions[x][0].state):
                    node = y
                    break
            assert node, 'group not found'
            r.add_transition(x, node[0].representative.value)
    end = [x for x in ds.groups if x[0].representative.value == initial][0]
    return end[0].representative.value
    
def from_lr1_to_lalr(lr1_automaton:State):
    pending = [s for s in lr1_automaton]
    ds = DisjointSet(*pending)
    while pending:
        to_merge = []
        pivot = center_of(pending[0].state)
        for i,x in enumerate(pending):
            if center_of(x.state) == pivot:
                to_merge.append(x)
                pending[i] = None
        pending = [x for x in pending if x]
        ds.merge(to_merge)

    for g in ds.groups:
        r = g[0].representative
        for x in [x for x in g if r != x]:
            for prod in r.value.state:
                for prod2 in x.value.state:
                    if prod.Center() == prod2.Center():
                        new_lookahead = {x for x in prod.lookaheads}
                        new_lookahead.update({x for x in prod2.lookaheads})
                        prod.lookaheads = frozenset(new_lookahead)
    return build_automaton_from_ds(lr1_automaton,ds)
        
def build_LALR1_automaton(G):
    return from_lr1_to_lalr(build_LR1_automaton(G))

class LALR1Parser(ShiftReduceParser):
    
    def __init__(self,G,verbose=False):
        super().__init__(G,build_LALR1_automaton,verbose)
        self.lr_type = 'lalr1'
    
    def _build_parsing_table(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
            
        automaton = self.automaton
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action,(idx,G.EOF),(self.OK,None))
                    else:
                        for c in item.lookaheads:
                            self._register(self.action, (idx,c),(self.REDUCE,item.production))
                else:
                    next_sym = item.NextSymbol
                    try:
                        next_state = node[next_sym.Name][0]
                        if next_sym.IsNonTerminal:
                            self._register(self.goto,(idx,next_sym),next_state.idx)
                        else:
                            self._register(self.action,(idx,next_sym),(self.SHIFT,next_state.idx))
                    except KeyError:
                        self.errors.append(f'Node: {node} without transition with symbol {next_sym}')
                        return None
        

############## Conflict Utils #######################
def go_back(state_to_transpose, symbol,expected_item,transpose_state_dic):
    """
    return a state that enter to state_to_transpose with symbol `symbol`
    """
    candidates = transpose_state_dic[state_to_transpose.idx][1][symbol.Name]
    candidates = [x for x in candidates if any([y for y in x.state if y.state == expected_item])]
    return transpose_state_dic[candidates[0].idx][0]

def find_path_to(goal_state,goal_item,current_state,current_item,path,item_checked):
    """
    path: a list of tuple (item's state, item) that represent th items taken to reach current state
    item_checked: a set of tuple (item, item's state.idx) that saves the visited  items
    return in path the items needed to reach the goal_item in goal_state from current_item in current_state
    """
    if goal_state == current_state and goal_item == current_item:
        return True
    if current_item.IsReduceItem:
        return False
    
    spanned_items = span_item(current_state,current_item)
    
    path.append((current_state[current_item[current_item.pos].Name][0],current_item.NextItem(),True if current_item[current_item.pos].IsNonTerminal else False))
    if not (path[-1][1],path[-1][0].idx) in item_checked:
        item_checked.add((path[-1][1],path[-1][0].idx))
        if find_path_to(goal_state,goal_item,path[-1][0],path[-1][1],path,item_checked):
            return True
    path.pop()
    
    for next_item in spanned_items:
        path.append((current_state,next_item,False))
        if not (path[-1][1],path[-1][0].idx) in item_checked:
            item_checked.add((next_item,current_state.idx))
            if find_path_to(goal_state,goal_item,path[-1][0],path[-1][1],path,item_checked):
                return True
        path.pop()
    return False

def items_to_terminals(first_path, second_path):
    """
    concat the terminals of first_path an the sentence of second_path
    """
    terminals = []
    for i,(state,item,skipped) in enumerate(first_path):
        if not item.IsReduceItem:
            if i != 0 and skipped: # before skiped:
                last_state,last_item,skipped = first_path[i-1]
                spanned_items = span_item(last_state,last_item)
                for next_item in spanned_items:
                    next_terminals = item_sentence(last_state,next_item)
                    if next_terminals:
                        terminals += next_terminals
                        break
            if item[item.pos].IsTerminal:
                terminals.append(item[item.pos])
                
    for state,item in second_path:
        if not item.IsReduceItem: 
            if item[item.pos].IsTerminal:
                terminals.append(item[item.pos])
            else:
                spanned_items = span_item(state,item)
                terminals += item_sentence(state,spanned_items[0])
    return terminals
    
def find_initial_item(initial_state):
    for in_state in initial_state.state:
        item = in_state.state
        if  len(item.production.Right) == 1 and item.production.Right[0].IsNonTerminal \
            and "'" in item.production.Left.Name:
            return item

def find_conflict_item(state,production):
    for in_state in state.state:
        if isinstance(in_state,Item):
            if in_state.production == production:
                return in_state
        else:
            item = in_state.state
            if item.production == production:
                return item

def span_item(state,item):
    return [x.state for x in state.state if x.state.production.Left == item[item.pos] and x.state.pos == 0] 
    # Tambien incluir los lookahead en la condicion?

def item_sentence(state,item):
    path = []
    _item_sentence(state,item,set(),path)
    return path

def _item_sentence(state:State,item,visited,path):
    
    if item.IsReduceItem:
        return True
    
    next_symb = item.NextSymbol
    if isinstance(next_symb,NonTerminal):
        if not (state.idx,next_symb) in visited:
            visited.add((state.idx,next_symb))
            for next_item in span_item(state,item):
                if _item_sentence(state,next_item,visited,path):
                    if _item_sentence(state[next_symb.Name][0],item.NextItem(),visited,path):
                        return True
    else:
        path.append(next_symb)
        if _item_sentence(state[next_symb.Name][0],item.NextItem(),visited,path):
            return True
        path.pop()