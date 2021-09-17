from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal)
from cmp.utils import ContainerSet, inspect, pprint, Token
from cmp_tools.utils.first_follow import compute_firsts, compute_follows, compute_local_first
from cmp_tools.parser.parser import Parser
from cmp_tools.grammar.grammar_fixer import fix_non_derive_terminal, build_reach

class ParserLL1(Parser):

    grammar = None

    firsts = None

    follows = None

    parse_table = None

    parser = None
    
    errors = []
    
    eval_errors = []

    def __init__(self, G:Grammar):
        """
        When created check for grammar errors in errors
        """
        self.grammar = G

    @property
    def get_follows(self):
        if self.follows is None:
            self.firsts = self.get_firsts
            self.follows = compute_follows(self.grammar,self.firsts)
        return self.follows            
    
    @property
    def get_firsts(self):
        if self.firsts is None:
            self.firsts = compute_firsts(self.grammar)
        return self.firsts  

    @property
    def get_parser_table(self):
        if self.parse_table is None:
            self.parse_table = self.build_parsing_table()
        return self.parse_table

    def __call__(self,tokens,errors):
        if not self.parser:
            self.parser = self.metodo_predictivo_no_recursivo()
        return self.parser(tokens,errors)
    
    def build_parsing_table(self):
        # init parsing table
        M = {}
        
        G = self.grammar
        firsts = self.get_firsts
        follows = self.get_follows

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            ###################################################
            # working with symbols on First(alpha) ...
            ###################################################
            #                   <CODE_HERE>                   #
            for t in firsts[alpha]:
                try:
                    a = M[X,t]
                    if type(a) == type(list()):
                        self.errors.append(\
                            f'Grammar Ambiguity: M[{X},{t}] = {a}, and also must be M[{X},{t}] = {alpha}')
                        if not alpha in a:
                            a.append(alpha)
                    elif a != alpha:
                        self.errors.append(\
                            f'Grammar Ambiguity: M[{X},{t}] = {a}, and also must be M[{X},{t}] = {alpha}')
                        M[X,t] = [a,alpha]
                except KeyError:
                    M[X,t] = alpha
            ###################################################    

            ###################################################
            # working with epsilon...
            ###################################################
            #                   <CODE_HERE>                   #
            if firsts[alpha].contains_epsilon:
                for t in follows[X]:
                    try:
                        a = M[X,t]
                        if a != alpha:
                            self.errors.append(\
                                f'Grammar Ambiguity: M[{X},{t}] = {a}, and also must be M[{X},{t}] = {alpha}')
                            if type(a) == type(list()):
                                a.append(alpha)
                            else:
                                M[X,t] = [a,alpha]
                    except KeyError:
                        M[X,t] = alpha
            ###################################################

        # parsing table is ready!!!
        return M        

    def return_prod(self, left,right):
        for i,x in enumerate(left.productions,0):
            if x.Right == right:
                return left.productions[i]; 
        return None

    def metodo_predictivo_no_recursivo(self):

        G = self.grammar
        M = self.get_parser_table
        firsts = self.get_firsts
        follows = self.get_follows

        # parser construction...
        def parser(tokens, parser_errors:list):

            ###################################################
            # tokens ends with $ (G.EOF)
            ###################################################
            # init:
            stack = [G.EOF,G.startSymbol]

            cursor = 0
            output = []
            ###################################################

            # parsing tokens...
            # print((top, a))

            ###################################################
            #                   <CODE_HERE>                   #
            while cursor < len(tokens):
                top = stack.pop()
                a = tokens[cursor]
                prod = None
                if top.IsTerminal:
                    if a.token_type == top:
                        cursor+=1
                        continue
                    else:
                        parser_errors.append(f'Expected: {top}, Recieve: {a.token_type}')
                        break
                try:
                    prod = M[top,a.token_type]
                except KeyError:
                    parser_errors.append(f'M[{top},{a.token_type}] generate nothing: expected {[ x[1] for x in M if x[0] == top ]}')
                    break

                if a.token_type in firsts[prod]:
                    rev = prod[::-1]
                    for t in rev:
                        stack.append(t)
                    output.append(self.return_prod(top,prod))

                elif prod.IsEpsilon and a.token_type in follows[top]:
                    output.append(self.return_prod(top,prod))
                else:
                    parser_errors.append(f'{a.token_type} Not in follows[{top}]')
                    break

            ###################################################

            # left parse is ready!!!
            return output

        # parser is ready!!!
        return parser

    def _evaluate(self, production, left_parse, tokens, inherited_value=None):
        head, body = production
        attributes = production.attributes

        # Insert your code here ...
        # > synteticed = ...
        synteticed = [None for _ in attributes]
        # > inherited = ...
        inherited = [None]*(len(body)+1)
        # Anything to do with inherited_value?
        inherited[0] = inherited_value

        for i, symbol in enumerate(body, 1):
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
                    next_production = next(left_parse)
                except StopIteration:
                    self.eval_errors.append(f'left_parse stopped the iteration')
                    break
                if not symbol == next_production.Left:
                    self.eval_errors.append(f'{symbol} doesnt match with {next_production.Left}. Cant expand {symbol}')
                    break
                # Insert your code here ...
                if attributes[i]:
                    inherited[i] = attributes[i](inherited, synteticed)
                synteticed[i] = self._evaluate(next_production, left_parse, tokens, inherited[i])

        # Insert your code here ...
        if attributes[0]:
            synteticed[0] = attributes[0](inherited, synteticed)
        # > return ...
        return synteticed[0]

    def evaluate_parse(self, left_parse, tokens):
        self.eval_errors.clear()
        if not left_parse or not tokens:
            self.eval_errors.append('Empty tokens or Empty left_parse')
            return None

        left_parse = iter(left_parse)
        tokens = iter(tokens)
        result = self._evaluate(next(left_parse), left_parse, tokens)

        if not isinstance(next(tokens).token_type, EOF):
            self.eval_errors.append('Last parsed token doesnt match with EOF')
            return None
        return result
    
    def evaluate(self,tokens,errors:list):
        """
        If no errors then returns the evaluated tokens\n
        else fills errors with errors returning None
        """
        parser = self.metodo_predictivo_no_recursivo()
        new_errors = []
        left_parse = parser(tokens,new_errors)
        if not new_errors:
            ast = self.evaluate_parse(left_parse, tokens)
            if self.eval_errors:
                for x in self.eval_errors:
                    errors.append(x)
                return None
            return ast.evaluate()
        else:
            for x in new_errors:
                errors.append(x)
            return None

    def find_conflict(self):
        table = self.get_parser_table
        conflicts = []
        for x in table:
            if type(table[x]) == type([1,2]):
                grammar,derive = fix_non_derive_terminal(self.grammar,True)
                visited = set([grammar.startSymbol,])
                conflict = self._find_conflict(build_reach(self.grammar,x[0]), grammar.startSymbol,x,derive,visited,[])
                conflicts.append(conflict)
        return conflicts
   
    def _find_conflict(self, reach, current, searching, derive, visited, productions):
        """
        si X in reach => X puede alcanzar a searching
        derive[X] producciones para hacer X una oracion
        searching llave de la tabla que da problemas
        productions producciones que va llevando
        """
        if current == searching[0]:
            return self._generate_conflict_error(searching,productions,derive)
            
        for x in current.productions:
            new_productions = productions.copy()
            new_productions.append(x)
            for y in x.Right:
                if y in reach:
                    if y not in visited:
                        visited.add(y)
                        conflict = self._find_conflict(reach,y,searching,derive,visited,new_productions)
                        if conflict:
                            return conflict
                        visited.remove(y)
                new_productions.extend(derive[y])
        
        return ''
        
    def _generate_conflict_error(self,searching,productions,derive):
        string = self._generate_conflict_string(productions,derive)
        aux = ' | '.join([str(x) for x in self.get_parser_table[searching]])
        conflict = f'The prefix "{string}{searching[1].Name}" generate the parse {productions}, that can be continued by these productions {searching[0]} -> {aux}'
        return conflict
    
    def _generate_conflict_string(self,productions,derive):

        stack = [self.grammar.startSymbol]
        cursor = 0
        output = []
        string = []
        
        while cursor < len(productions):
            top = stack.pop()
            
            if top.IsTerminal:
                if not top.IsEpsilon:
                    string.append(top)
                cursor += 1
                continue
            
            prod = productions[cursor]
            
            if prod.Right:
                rev = prod.Right[::-1]
                for t in rev:
                    stack.append(t)
            else:
                stack.append(self.grammar.Epsilon)
            cursor += 1
        
        stack.reverse()
        for x in stack:
            if x.IsTerminal:
                string.append(x)
        
        output = ''
        for x in string:
            output += x.Name + ' '
            
        return output
