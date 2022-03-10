from typing import List
from generated_utils.token_class import Match, Token, tokenizer
from generated_utils.serializer_class import Serializer

class LexerTable(list, Serializer):
    def __init__(self, ignore, eof, eoline):
        super(LexerTable, self).__init__()
        self.ignore = ignore
        self.eof = eof
        self.eoline = eoline

class Lexer:
    def __init__(self,match:Match,token_type=None):
        if token_type:
            globals()["TOKEN_TYPE"] = token_type
        
        self.table:LexerTable = LexerTable.deserializer("{Wp48S^xk9=GL@E0stWa761SMbT8$j-~pBZ^IZTy0LTN4G=3m`j8;Q?z*2E#Wj_88)8P%4GwwAy3|RJ3Rgr_*N;L%%A`S%iO02?=w)y+;ZSjB4DXt)7zo}tq;jQj^okOWE?RA%N>HuW*9uT6GCo$N~U>HT<JNb>t(L{=V*cE6YHnJ6j==%Y@mA=CS&f?YKl>aIaKf=O>K3mc^$^NSPAd)nH3)lpZDv*6<tftnNWpu>a<xrZT|6aoO-P1)XmeDjbUBhe$_(in`VhX#@T!wW+&+ZbRx;}C0n?J%XV4`+ag}We){7GED9<^*vEe`9LmKPKu1(&J{)-|)`mbRvclN7y4J~99RC-&dHHgyg)00EBzmjeI*^hTm|vBYQl0ssI200dcD")
        self.match:Match=match
        for t in self.table:
            if t[0] != self.table.eof:
                self.match.add_matcher(t)
        self.match.initialize()

    def __call__(self,input:str) ->List[Token]:
        token_list,errors= tokenizer(input,self.table.ignore,self.table.eof,self.table.eoline,self.match)
        return token_list,errors
