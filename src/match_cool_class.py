from typing import List, Tuple
from main_regex import RegexCompilator, RegexExpr
from match_class import Match

class CoolMatch(Match):
        def __init__(self):
            self.match_ = dict()
            self.compiled: List[Tuple[str, RegexExpr]] | None = None
            self.reg_comp = RegexCompilator()    
        
        def add_matcher(self, to_add):
            if not self.compiled:
                self.match_[to_add[0]] = to_add[1:]

        def initialize(self):
            if self.compiled is None:
                self.compiled = []
                for name, matcher in self.match_.items():
                    regex = matcher[0]
                    pattern = self.reg_comp.compile(regex)
                    self.compiled.append((name, pattern))

        def match(self, match, pos):
            matched_expr=""
            matched_str=None
            matched_bool=False
            for str_,expr in self.compiled:
                match_,bool_match_= expr.match(match,pos)
                if len(match_)>len(matched_expr) or (len(match_)==len(matched_expr) and not matched_bool and bool_match_):
                    matched_str=str_
                    matched_expr =match_
                    matched_bool=bool_match_
            
            matched_extra=(False,[])       
            if matched_bool:
                matched_extra = self.match_[matched_str][1] if self.match_[matched_str][1] else matched_extra
            return (matched_str, matched_expr, matched_extra,matched_bool)