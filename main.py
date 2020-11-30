import streamlit as st
from cmp.grammar import G
from cmp.lexer import tokenize_text, pprint_tokens
from cmp.tools import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from cmp.formatter import FormatVisitor
from cmp.type_collector import TypeCollector
from cmp.type_builder import TypeBuilder
from cmp.type_checker import TypeChecker
from cmp.type_inferencer import TypeInferencer


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
    manager = builder.manager
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    print('Context:')
    print(context)
    print('=============== CHECKING TYPES ================')
    checker = TypeChecker(context, manager, [])
    scope = checker.visit(ast)
    print('=============== INFERING TYPES ================')
    temp_errors = []
    inferencer = TypeInferencer(context, manager, temp_errors)
    inferencer.visit(ast, scope)
    print('Errors: [')
    for error in temp_errors:
        print('\t', error)
    print(']')
    print('=============== LAST CHECK ================')
    errors.extend(temp_errors)
    checker = TypeChecker(context, manager, errors)
    checker.visit(ast)
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    
    return ast


text = '''
class A {
    f ( a : AUTO_TYPE , b : AUTO_TYPE ) : AUTO_TYPE {
        if ( a = 1 ) then b else
            g ( a + 1 , b / 2 )
        fi
    } ;
    g ( a : AUTO_TYPE , b : AUTO_TYPE ) : AUTO_TYPE {
        if ( b = 1 ) then a else
            f ( a / 2 , b + 1 )
        fi
    } ;
} ;
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

            st.subheader('Building types')
            builder = TypeBuilder(context, errors)
            builder.visit(ast)
            manager = builder.manager
            for e in errors:
                st.error(e)
            st.text('Context:')
            st.text(context)

            st.subheader('Checking types')
            checker = TypeChecker(context, manager, [])
            scope = checker.visit(ast)

            st.subheader('Infering types')
            temp_errors = []
            inferencer = TypeInferencer(context, manager, temp_errors)
            inferencer.visit(ast, scope)
            for e in temp_errors:
                st.error(e)

            st.subheader('Las check')
            errors.extend(temp_errors)
            checker = TypeChecker(context, manager, errors)
            checker.visit(ast)
            for e in errors:
                st.error(e)
                
            formatter = FormatVisitor()
            tree = formatter.visit(ast)
            st.text(tree)


        except Exception as e:
            st.error(f'Unexpected error!!! You probably did something wrong :wink:')


if __name__ == '__main__':
    # main(G)
    ast = run_pipeline(G, text)