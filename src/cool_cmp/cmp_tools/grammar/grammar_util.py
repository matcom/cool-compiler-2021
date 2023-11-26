from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal)
from cmp_tools.grammar.grammar_parser import expand


def grammar_to_text(G:Grammar):
    gram = ''
    for n in G.nonTerminals:
        gram += n.Name + f' {expand} '
        for p in n.productions:
            if p.Right.IsEpsilon:
                gram += ' epsilon '
            else:
                for s in p.Right:
                    gram += f' {s.Name} '
            gram += ' | '
        gram = gram[:len(gram)-2]
        gram += ';\n'
        
    return gram
                