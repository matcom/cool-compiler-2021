from cmp.grammar import G
from cmp.lexer import tokenize_text, pprint_tokens
from cmp.tools import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from cmp.formatter import FormatVisitor


def run_pipeline(G, text):
    print('=================== TEXT ======================')
    print(text)
    print('================== TOKENS =====================')
    tokens = list(tokenize_text(text))
    pprint_tokens(tokens)
    print('=================== PARSE =====================')
    parser = LR1Parser(G)
    parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
    print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    return ast


text = '''
    class A {
        a : Z ;
        suma ( a : int , b : B ) : int {
            a + b
        } ;
        b : int <- 9 ;
        c : C ;
    } ;

    class B inherits A {
        c : A ;
        f ( d : int , a : A ) : void {
            {
                let f : int <- 8 in f + 3 * d ;
                c <- suma ( 5 , f ) ;
            }
        } ;
        z : int ;
    } ;

    class C inherits Z {
    } ;
'''

if __name__ == '__main__': ast = run_pipeline(G, text)