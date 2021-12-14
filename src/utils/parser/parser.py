from cmp.utils import ContainerSet
from cmp.pycompiler import Sentence
from itertools import islice
from collections import deque

class Parser:
    def __init__(self,G):
        self.G = G
        if not self.action:
            self.firsts = self.compute_firsts()
            self.follows = self.compute_follows()
            self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()
    
    def _find_conflict(self):
        raise NotImplementedError()
    
    # Computes First(Vt) U First(Vn) U First(alpha)
    # P: X -> alpha
    def compute_firsts(self):
        firsts = {}
        change = True
        
        # init First(Vt)
        for terminal in self.G.terminals:
            firsts[terminal] = ContainerSet(terminal)
            
        # init First(Vn)
        for nonterminal in self.G.nonTerminals:
            firsts[nonterminal] = ContainerSet()
        
        while change:
            change = False
            
            # P: X -> alpha
            for production in self.G.Productions:
                X = production.Left
                alpha = production.Right
                
                # get current First(X)
                first_X = firsts[X]
                    
                # init First(alpha)
                try:
                    first_alpha = firsts[alpha]
                except:
                    first_alpha = firsts[alpha] = ContainerSet()
                
                # CurrentFirst(alpha)???
                local_first = self.compute_local_first(firsts, alpha)
                
                # update First(X) and First(alpha) from CurrentFirst(alpha)
                change |= first_alpha.hard_update(local_first)
                change |= first_X.hard_update(local_first)
                        
        # First(Vt) + First(Vt) + First(RightSides)
        return firsts

    # Computes First(alpha), given First(Vt) and First(Vn) 
    # alpha in (Vt U Vn)*
    def compute_local_first(self,firsts, alpha):
        first_alpha = ContainerSet()
        
        try:
            alpha_is_epsilon = alpha.IsEpsilon
        except:
            alpha_is_epsilon = False
        
        # alpha == epsilon ? First(alpha) = { epsilon }
        if alpha_is_epsilon:
            first_alpha.set_epsilon()

        # alpha = X1 ... XN
        # First(Xi) subconjunto First(alpha)
        # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
        # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
        else:
            for item in alpha:
                first_symbol = firsts[item]
                first_alpha.update(first_symbol)
                if not  first_symbol.contains_epsilon:
                    break
            else:
                first_alpha.set_epsilon()
        
        # First(alpha)
        return first_alpha
    

    def compute_follows(self):
        follows = { }
        change = True
        
        local_firsts = {}
        
        # init Follow(Vn)
        for nonterminal in self.G.nonTerminals:
            follows[nonterminal] = ContainerSet()
        follows[self.G.startSymbol] = ContainerSet(self.G.EOF)
        
        while change:
            change = False
            
            # P: X -> alpha
            for production in self.G.Productions:
                X = production.Left
                alpha = production.Right
                
                follow_X = follows[X]
                
                # X -> zeta Y beta
                # First(beta) - { epsilon } subset of Follow(Y)
                # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
                for i,symbol in enumerate(alpha):
                        if symbol.IsNonTerminal:
                            follow_Y = follows[symbol]
                            try:
                                firts_beta = local_firsts[alpha,i]
                            except KeyError:
                                firts_beta = local_firsts[alpha,i] = self.compute_local_first(self.firsts,islice(alpha,i+1,None))

                            change |= follow_Y.update(firts_beta)

                            if firts_beta.contains_epsilon:
                                change |= follow_Y.update(follow_X)

        # Follow(Vn)
        return follows