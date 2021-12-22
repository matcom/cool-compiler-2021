from TOKEN import LexToken

class Lexer:
    def __init__(self,text):
        self.my_bool = False
        self.result = ''
        self.names = {
            "case" : "CASE",
            "class" : "CLASS",
            "else" : "ELSE",
            "esac" : "ESAC",
            "fi" : "FI",
            "if" : "IF",
            "in" : "IN",
            "inherits" : "INHERITS",
            "isvoid" : "ISVOID",
            "let" : "LET",
            "loop" : "LOOP",
            "new" : "NEW",
            "of" : "OF",
            "pool" : "POOL",
            "then" : "THEN",
            "while" : "WHILE",
            "not" : "NOT",
            "true" : "TRUE",
            "false" : "FALSE",
            "(" : "LPAREN",
            ")" : "RPAREN",
            "{" : "LBRACE",
            "}" : "RBRACE",
            ":" : "TDOTS",
            "," : "COMMA",
            "." : "DOT",
            ";" : "SEMICOLON",
            "@" : "AT",
            "*" : "MULTIPLY",
            "/" : "DIVIDE",
            "+" : "PLUS",
            "-" : "MINUS",
            "~" : "INT_COMP",
            "<" : "LT",
            "=" : "EQ",
            "<=" : "LTEQ",
            "<-" : "ASSIGN",
            "=>" : "ARROW", }
        self.token_list = []
        self.Simple_tokens = ['(', ')', '{', '}', ':', ',','.',';','@','*','/','+','-','~','<','=','<=','<-','=>']
        self.error_tokens = ['!','$','%','^','?','[',']','#','&']
        self.ABC = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.abc = [str.lower(item) for item in self.ABC]
        self._int = ['0','1','2','3','4','5','6','7','8','9']
        self.get_tokens(text)
        
    def error(self,line,column,value):
        message = f'({line}, {column}) - LexicographicError: ERROR "'
        message += value
        message +='"'
        if self.result =='':
            self.result = message
        self.my_bool = True

    def error_String_null(self,line,column):
        if self.result=='':
            self.result = f'({line}, {column}) - LexicographicError: String contains null character'
        self.my_bool = True

    def error_Comment_EOF(self,line,column):
        if self.result=='':
            self.result = f"({line}, {column}) - LexicographicError: EOF in comment"
        self.my_bool = True

    def error_String_EOF(self,line,column):
        if self.result=='':
            self.result = f'({line}, {column}) - LexicographicError: EOF in string constant'
        self.my_bool = True

    def error_String_New_Line(self,line,column):
        if self.result == '':
            self.result = f'({line}, {column}) - LexicographicError: Unterminated string constant'
        self.my_bool = True

    def get_tokens(self,text):
        i=-1
        n = len(text)
        Ln = 1
        Col = 1
        current1 = ''
        current2 = ''
        open_comments = 0
        while i < n - 1:
            
            i += 1

            if text[i] in self.error_tokens:
                Col+=len(current1)
                self.error(Ln, Col, text[i])
                break

            if text[i] == '\t': 
                Col+=1
                continue
            
            if text[i] == ' ':
                Col+=1
                continue
            
            if text[i] == '\n':                         #end line
                Col=1
                Ln+=1
                continue
            
            if text[i] == '-' and text[i + 1] == '-':   #ignore comment
                while not text[i] == '\n': i+=1
                Col=1
                Ln+=1
                continue
            
            if text[i] == '(' and text[i + 1] == '*':   #ignore comment
                open_comments += 1
                while open_comments > 0:
                    i+=1
                    Col+=1
                    if i == len(text):
                        self.error_Comment_EOF(Ln,Col)
                        i=len(text)             #end
                        break
                    if text[i] == '\n':
                        Ln+=1
                        Col=0
                    if text[i] == '(' and text[i + 1] == '*':
                        open_comments += 1
                    if text[i] == '*' and text[i + 1] == ')':
                        i+=1
                        open_comments -= 1
                continue
            
            if text[i] == '"':
                
                i+=1
                length = 1

                if i==len(text):
                    Col+=length
                    self.error_String_EOF(Ln,Col)
                    break

                while not text[i] == '"':            
                    
                    if text[i] == '\n':
                        Col+=length
                        self.error_String_New_Line(Ln,Col)
                        i=len(text)
                        break

                    if text[i]=='\0':
                        Col+=length
                        self.error_String_null(Ln,Col)
                        i=len(text)
                        break

                    if text[i]=='\\':                    
                        if not text[i+1]=='b' and not text[i+1]=='t' and not text[i+1]=='n' and not text[i+1]=='f':
                            
                            current1+=text[i+1]
                            length+=2

                            if text[i+1]=='\n': 
                                Ln+=1
                                Col=0
                                length=1

                            i+=2
                            continue
                    
                    current1 += text[i]
                    length+=1            
                    i+=1
                    if i==len(text):
                        Col+=length
                        self.error_String_EOF(Ln,Col)                
                        break
                
                self.token_list.append(LexToken('STRING',current1,Ln,Col))
                Col+=length + 1
                current1 = ''
                continue

            current1 += text[i]

            if i + 1 < len(text): current2 = current1 + text[i + 1]
            else: current2 = current1

            _next = current2[-1]    #text[i + 1]

            if current1[0] == '_':
                self.error(Ln,Col,current1[0])
                break

            if current1[0] in self._int:
                i+=1
                while text[i] in self._int:
                    current1 += text[i]
                    i+=1
                i-=1
                self.token_list.append(LexToken('INTEGER',int(current1), Ln,Col))
                Col+=len(current1)
                current1 = ''
                continue
        
            if current2 in self.Simple_tokens:
                self.token_list.append(LexToken(self.names[current2],current2,Ln,Col))
                Col+=len(current2)
                i+=1
                current1 = ''
                continue

            if current1 in self.Simple_tokens:
                self.token_list.append(LexToken(self.names[current1],current1,Ln,Col))
                Col+=len(current1)
                current1 = ''
                continue

            if _next in self.Simple_tokens or _next == ' ' or _next == '\n' or _next == '\t' or i+1==len(text):

                lower = str.lower(current1)
                
                if self.names.__contains__(lower):
                    self.token_list.append(LexToken(self.names[lower],lower,Ln,Col))
                    Col+=len(current1)
                    current1 = ''
                    continue
                
                if current1[0] in self.ABC:
                    self.token_list.append(LexToken('TYPE',current1,Ln,Col))
                    Col+=len(current1)
                    current1 = ''
                    continue
                
                if current1[0] in self.abc:
                    self.token_list.append(LexToken('ID',current1,Ln,Col))
                    Col+=len(current1)
                    current1 = ''

