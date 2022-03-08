from typing import List

from token_class import Token, tokenizer
from match_class import Match
from serializer_class import Serializer

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
        
        self.table:LexerTable = LexerTable.deserializer("{Wp48S^xk9=GL@E0stWa761SMbT8$j;0B5VUtIt|0LTN4G=3m`j8;Q?z*2E#Wj_88)8P%4GwwAy3|RJ3Rgr_&jy`#Iwhg#uD2sX(88SgGREIP@X(2SoOf8clL4%oMTvyBEd=fcS6Lt*;FiOq6&#f8(tpb$f?qgVL@IZcPjH-;eZb+F#b!#(y%3G-@;2sRnSx~!fKtObec3~@aJ|20f`V44`{gE)jf3A%VS47KItY=iD)>wuXY~hx<Ey?j!XKKYINRl%o?tOC;V-Txa!d&3LgMQ32fdSF;fF)&j?fS#xM9V(&(x@9lWhbivu4|)JLL12L$<U%iH8Z!jwKc28_K3{y?Uncr`BWvSJ7<ap)?kEIm=RrZOAwbmsbmuI7^>%EJ5el(9BDc3cGn07X1${mI{)L@-#Ot5XwAIC0tZ2{3Q-;f1PzCkU`fN#GOb^RkyKGj#j*yC4meEl>xqXTCMBXODT<#VEuJ&an~ynV!(qz}SgEN9I8a5a*8unpK=-Yi)PN<x<h1Hdkdeq6t$Tsmc*8K|jUW?w$&h;w>py(f$N2Ig(jNo$k@eG@<2=swDud1@Huo+sX2kc9GP{hDJoSXNjB2l%M4$1Ee5ZR>GSg{1qb<d-FA`V^P`PVcQHYDaMFAI{Mzk*D=};w0U~CIu&H5tyMyzvw-c>Fc+u!lW6qDU#Chec1sZ!)xFF5}#fD*(zaFv59DlIPWVtIW~41mHPu_PNY=&(SiIpQ6u%SHc2!aeiLFn0%3ND4(ag`)D7B2;rcQd%JDhkMiK7RDr%bXr&Cx?Fkpc3kqeF1Oowb@k`TfnXsd8ZD-MF+a*82D2C2&=XUd#x~;K$_sX67tmReVu<v2pE1HK2CUNTSJi{I)C9%AJ_f_21NNp`_aiMXm-^v<iNRJbbGA?-^@YS@!D1rycN2k{lJ0;Lc5YtiN2hm(r|vgko)Eql4pcn}qL%Y}S7x)U9epl-6o~h#N=YD~484NU0oXu=fhDt$c9V+cWR1rhK|yb5^B!<{8tM+lWmyhlwKs&-zki}%d27#!k!)c2N?Sbxlr?arIe7tpEfUdy-dTVoHWt`}v{vP@)wd^NRH_2U(@(XY3C<AX(CABCQ2#(}ZK3aoZ}Mv4(%v!rj^=bgL~j59;3GctvrNgD00H|3iwyt(&T7B`vBYQl0ssI200dcD")
        self.match:Match=match
        for t in self.table:
            if t[0] != self.table.eof:
                self.match.add_matcher(t)
        self.match.initialize()

    def __call__(self,input:str) ->List[Token]:
        token_list,errors= tokenizer(input,self.table.ignore,self.table.eof,self.table.eoline,self.match)
        return token_list,errors
