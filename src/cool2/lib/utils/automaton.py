from cmp.utils import ContainerSet
from cmp.utils import DisjointSet
from cmp.automata import State
import pydot

def state_transpose(initial_state:State):
    """
    returns the state equivalent to initial_state on the transpose graph and a dictionary mapping idx to new states transposed
    """
    state_dict = {} # state_dict[key] = (original_state,copy_of_original_state_with_transposed_transitions)
    idx = 0
    for x in initial_state:
        new_state = State(x.state,x.final,x.formatter,x.shape)
        if not hasattr(x,'idx'):
            x.idx = idx
            idx+=1
        new_state.idx = x.idx
        state_dict[x.idx] = (x,new_state)
    
    for x in initial_state:
        for key,states in x.transitions.items():
            for state in states:
                state_dict[state.idx][1].add_transition(key,state_dict[x.idx][1])
    
    return state_dict[initial_state.idx][1],state_dict
          
class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        # G = 'Graph Drawed'
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        # Your code here
        try:
            self.current = self.transitions[self.current][symbol][0]
            return True
        except: # Ver el error q da
            return False
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        # Your code here
        self._reset()
        for i in range(0,len(string)):
            if not self._move(string[i]):
                return False                       
        return self.current in self.finals

def goto(automaton:NFA, states, symbol):
    # Devuelve los estados en los cuales existe una transicion desde alguno de los estados de states mediante
    # symbol
    moves = set()
    for state in states:
        # Your code here
        try:
            for i in automaton.transitions[state][symbol]:
                moves.add(i)
        except:
            pass
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    analiced = [False]*automaton.states

    while pending:
        state = pending.pop()
        # Your code here
        try:
            for i in automaton.transitions[state]['']:
                if not analiced[i]:
                    closure.add(i)
                    pending.append(i)
        except KeyError: # Ver el error q da
            pass
        analiced[state] = True
    return ContainerSet(*closure)

def first(cond, itera):
    for x in iter(itera):
        if cond(x):
            return x
    return None

def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]
    pending = [ start ]
    ids = 1
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            # Your code here
            # ...
            new_state = epsilon_closure(automaton,goto(automaton, state, symbol))
            
            if len(new_state) == 0: # no genera nada
                continue
            
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                if new_state in states:
                    transitions[state.id, symbol] = first(lambda x: x.set == new_state.set,states).id
                    continue

                new_state.id = ids
                ids += 1
                new_state.is_final = any(s in automaton.finals for s in new_state)
                transitions[state.id, symbol] = new_state.id
            
                pending.append(new_state) # agregar id al new_state
                states.append(new_state)

    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[origin + d1,symbol] = [t for t in map(lambda x: x+d1,destinations)]
            

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        # Your code here
        transitions[origin + d2,symbol] = [t for t in map(lambda x: x+d2,destinations)]
    
    ## Add transitions from start state ...
    # Your code here
    transitions[start,''] = [a1.start + d1, a2.start + d2] # epsilon transitions to initials of a1 and a2

    ## Add transitions to final state ...
    # Your code here
    for f1 in a1.finals:
        try:
            transitions[f1 + d1,''].append(final)
        except KeyError:
            transitions[f1 + d1,''] = [final]

    for f2 in a2.finals:
        try:
            transitions[f2 + d2,''].append(final)
        except KeyError:
            transitions[f2 + d2,''] = [final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[origin + d1, symbol] = [t for t in map(lambda x: x+d1,destinations)]

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        # Your code here
        transitions[origin + d2, symbol] = [t for t in map(lambda x: x+d2,destinations)]
        
            
    ## Add transitions to final state ...
    # Your code here
    for f1 in a1.finals:
        try:
            transitions[f1 + d1,''].append(a2.start + d2)
        except KeyError:
            transitions[f1 + d1,''] = [a2.start + d2]

    for f2 in a2.finals:
        try:
            transitions[f2 + d2,''].append(a2.start + d2)
        except KeyError:
            transitions[f2 + d2,''] = [final]           
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate automaton transitions ...
        # Your code here
        transitions[origin + d1,symbol] = [t for t in map(lambda x: x+d1,destinations)]
    
    ## Add transitions from start state ...
    # Your code here
    transitions[start,''] = [a1.start + d1, final]
    
    ## Add transitions to final state and to start state ...
    # Your code here
    for f1 in a1.finals:
        try:
            transitions[f1 + d1,''].append(a1.start + d1)
            transitions[f1 + d1,''].append(final)
        except:
            transitions[f1 + d1,''] = [a1.start + d1]
            transitions[f1 + d1,''].append(final)
            
    
    states = a1.states +  2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)
    for member1 in group:
        # Your code here
        # mira a ver a que grupo pertenece
        for group_representative in split.keys():
            # chequea el vocabulario
            for symbol in vocabulary:
                err1, err2 = False, False
                try:
                    m1 = automaton.transitions[partition[group_representative].value][symbol][0]
                except KeyError:
                    err1 = True
                try:
                    m2 = automaton.transitions[member1.value][symbol][0] 
                except KeyError:
                    err2 = True
                
                if err1 and err2:
                    continue
                elif (not err1 and err2) or (err1 and not err2):
                    break
                
                if partition[m1].representative != partition[m2].representative:
                    break
            else:
                # matcheo todo el vocabulario
                split[group_representative].append(member1.value)
                break                
        else:
            # no pertenece a ninguno por lo tanto creo uno nuevo
            split[member1.value] = [member1.value]
    return [group for group in split.values()]

def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    ## partition = { NON-FINALS | FINALS }
    # Your code here
    partition.merge([ x for x in automaton.finals])

    non_finals = [nf for nf in filter(lambda x: not x in automaton.finals,range(automaton.states))]
    partition.merge(non_finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        
        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        # Your code here
        for gr in partition.groups:
            for gr in distinguish_states(gr,automaton,partition) :
                new_partition.merge(gr)

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)
    
    states = [s for s in partition.representatives]
    transitions = {}
    
    for i, state in enumerate(states):
        # Your code here
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            # Your code here
            transition = states.index(partition[destinations[0]].representative)
            
            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                # Your code here
                transitions[i,symbol] = transition
    
    # Your code here
    finals = set()
    for gr in partition.groups:
        for i in gr:
            if i.value in automaton.finals:
                finals.add(states.index(i.representative))
    start = states.index(partition[automaton.start].representative) 
    
    return DFA(len(states), finals, transitions, start)

def automata_full_determined(a1):
    transitions = {}
    
    if a1.states * len(a1.vocabulary) == len(a1.map.items()):
        for (origin, symbol), destinations in a1.map.items():
            # Your code here
            transitions[origin,symbol] = [t for t in destinations]
    
        return NFA(a1.states,a1.finals,transitions,a1.start)
    
    
    start = 0
    # final = a1.states
    end = a1.states #final + 1
    
    for (origin, symbol), destinations in a1.map.items():
        # Your code here
        transitions[origin,symbol] = [t for t in destinations]
    
    
    for i in range(end):
        for x in a1.vocabulary:
            try:
                transitions[i,x]
            except KeyError:
                transitions[i,x] = [end]
    
    for v in a1.vocabulary:
        try:
            transitions[end,v].append(end)
        except KeyError:
            transitions[end,v] = [end]
    
    states = a1.states +  1
    finals = set(a1.finals)
    
    return NFA(states, finals, transitions, start)

def automata_complement(a1):
    a1 = automata_full_determined(a1)
    transitions = {}
    
    start = a1.start
    final = a1.states # a1.states estado epsilon
    
    for (origin, symbol), destinations in a1.map.items():
        # Your code here
        transitions[origin,symbol] = [t for t in destinations]
    
    for x in filter(lambda x: not x in a1.finals, range(a1.states)):
        transitions[x,''] = [final]
    
    states = a1.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_intersection(a1,a2):
    return automata_complement(automata_union(automata_complement(a1),automata_complement(a2)))

def automata_difference(a1,a2):
    return automata_intersection(a1,automata_complement(a2))

def automata_reverse(a1):
    transitions = {}
    
    start = a1.states
    final = a1.start
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate automaton transitions ...
        # Your code here
        for x in destinations:
            try:
                transitions[x,symbol].append(origin)
            except KeyError:
                transitions[x,symbol] = [origin]

    transitions[start,''] = [x for x in a1.finals]
            
    states = a1.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)
