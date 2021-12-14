from utils.parser.parser import Parser

class ShiftReduceParser(Parser):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G):
        try:
            self.action
        except AttributeError:
            self.action = {}
            self.goto = {}
            self.automaton = None

        self.error = ''
        Parser.__init__(self, G)

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        operations = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
                
            # (Detect error)
            
            try:
                action, tag = self.action[state, self.G[lookahead.token_type].Name]

                # (Shift case)
                if action == self.SHIFT:
                    stack.append(tag)
                    cursor += 1

                # (Reduce case)
                elif action == self.REDUCE:
                    tag = self.G.Productions[tag]
                    output.append(tag)
                    for _ in tag.Right: stack.pop()
                    a = self.goto[stack[-1], tag.Left.Name]
                    stack.append(a)


                # (OK case)
                elif action == self.OK:
                    return output, operations

                # (Invalid case)
                else:
                    raise Exception ['Error...']

                operations.append(action)

            except:
                self.error = f'({lookahead.line}, {lookahead.column}) - SyntacticError: ERROR at or near "{lookahead.lex}"'
                return None, None

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value