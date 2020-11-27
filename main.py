import streamlit as st
from cmp.grammar import G
from cmp.lexer import tokenize_text, pprint_tokens
from cmp.tools import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from cmp.formatter import FormatVisitor
from cmp.type_collector import TypeCollector
from cmp.type_builder import TypeBuilder


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
    print('============== COLLECTING TYPES ===============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print('Errors:', errors)
    print('Context:')
    print(context)
    print('=============== BUILDING TYPES ================')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    print('Context:')
    print(context)
    return ast


text = '''
    class A inherits C { } ;
    class C inherits B { } ;
    class B inherits A { } ;
    class B { } ;
    class B inherits A { } ;
'''

def main(G):
    st.title('Type Inferer')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    text = st.text_area('Input your code here:')

    if text:
        try:
            st.title('Results:')

            st.subheader('Tokens')
            tokens = list(tokenize_text(text))
            p_tokens = pprint_tokens(tokens, get=True)
            st.text(p_tokens)

            st.subheader('Parse')
            parser = LR1Parser(G)
            parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
            p_parse = '\n'.join(repr(x) for x in parse)
            st.text(p_parse)

            st.subheader('AST')
            ast = evaluate_reverse_parse(parse, operations, tokens)
            formatter = FormatVisitor()
            tree = formatter.visit(ast)
            st.text(tree)

            st.subheader('Collecting types')
            errors = []
            collector = TypeCollector(errors)
            collector.visit(ast)
            context = collector.context
            for e in errors:
                st.error(e)
            st.text('Context:')
            st.text(context)


        except Exception as e:
            st.error(f'Unexpected error!!! You probably did something wrong :wink:')


if __name__ == '__main__':
    main(G)
    # ast = run_pipeline(G, text)