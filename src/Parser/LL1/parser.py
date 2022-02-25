from Utils import *
from ..utils import *

class LL1Parser:    
    def build_ll1_table(G: Grammar, firsts, follows):
        # init parsing table
        M = {}
        is_ll1 = True
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            # working with symbols on First(alpha) ...
            first_alpha = firsts[alpha]
            for symbol in first_alpha:
                is_ll1 &= _register(M, X, symbol, production)
            
            # working with epsilon...
            if first_alpha.contains_epsilon:
                for symbol in follows[X]:
                    is_ll1 &= _register(M, X, symbol, production)
            
        # parsing table is ready!!!
        return M, is_ll1

    def nonrecursive_predictive_method(G, M, firsts, follows):
        # parser construction...
        def parser(w):
            
            # w ends with $ (G.EOF)
            # init:
            stack = [G.startSymbol]
            cursor = 0
            output = []
            
            # parsing w...
            while stack:
                top = stack.pop()
                a = w[cursor]
                
                if top.IsTerminal:
                    if top == a:
                        cursor += 1
                    else:
                        return None
                else:
                    try:
                        production = M[top][a][0]
                    except KeyError:
                        return None

                    output.append(production)
                    stack.extend(reversed(production.Right))
            
            # left parse is ready!!!
            return output
        
        # parser is ready!!!
        return parser
