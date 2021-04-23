
from cmp.utils import Token
from cmp.automata import State
from lib.lexer.regex import regex_automaton

class DetailToken(Token):
    def __init__(self, lex,token_type):
        super().__init__(lex,token_type)
        self.row = lex[1]
        self.column = lex[2]

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
        self.table = { x:y for x,y in table}
    
    def _build_regexs(self, table):
        regexs = {}
        for n, (token_type, regex) in enumerate(table):
            # Your code here!!!
            # - Remember to tag the final states with the token_type and priority.
            # - <State>.tag might be useful for that purpose ;-)
            auto = regex_automaton(regex)
            auto, states = State.from_nfa(auto,True)
            for st in states:
                if st.final:
                    st.tag = (n,token_type)
            regexs[token_type] = auto
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        # Your code here!!!
        for x in self.regexs:
            start.add_epsilon_transition(self.regexs[x])
        return start.to_deterministic()
    
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            # Your code here!!!
            if state.has_transition(symbol):
                state = state[symbol][0]
                if state.final:
                    final = state  
                    final_lex = lex
                # else:
                #     final = None
            else:
                final_lex = lex
                break
            lex += symbol
        else:
            final_lex = lex
            
        return final, final_lex
    
    def _tokenize(self, text):
        
        while text:
            stop_state, lex = self._walk(text)
            
            if stop_state and len(lex)>0:
                st_min = min([st.tag for st in [ final for final in stop_state.state if final.final]]) 
                yield lex,st_min[1]
            else:
                if len(lex) == 0:
                    lex = text[0]
                yield lex,'UNKNOWN'

            text = text[len(lex):]
            
        yield '$', self.eof
         
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]

class DetailLexer(Lexer):
    
    def _tokenize(self, text):
        row,column = 0,0
        while text:
            stop_state, lex = self._walk(text)
            
            rows_in_lex = len([x for x in lex if x == '\n'])
            row += rows_in_lex
            if rows_in_lex:
                column = len(lex.split('\n')[-1])
            else:
                column += len(lex)
            
            if stop_state and len(lex)>0:
                st_min = min([st.tag for st in [ final for final in stop_state.state if final.final]]) 
                yield (lex,row,column),st_min[1]
            else:
                if len(lex) == 0:
                    lex = text[0]
                yield (lex,row,column),'UNKNOWN'

            text = text[len(lex):]
            
        yield ('$',row,column), self.eof
 
    def __call__(self, text):
        return [ DetailToken(lex, ttype) for lex, ttype in self._tokenize(text) ]


nonzero_digits = '[123456789]'
min_letters = '[abcdefghijklmnopqrstuvwxyz]'
cap_letters = '[ABCDEFGHIJKLMNOPQRSTUVWXYZ]'
digits = f'({nonzero_digits}|0)'
