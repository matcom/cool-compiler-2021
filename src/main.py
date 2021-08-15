import streamlit as st
from compiler.cmp.grammar import G
from compiler.lexer.lexer import tokenize_text, pprint_tokens
from compiler.cmp.tools import LR1Parser
from compiler.cmp.evaluation import evaluate_reverse_parse
from compiler.visitors.formatter import FormatVisitor
from compiler.visitors.type_collector import TypeCollector
from compiler.visitors.type_builder import TypeBuilder
from compiler.visitors.type_checker import TypeChecker
from compiler.visitors.type_inferencer import TypeInferencer


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
class Main inherits IO {
    number: Int <- 5;

    main () : Object {
        testing_fibonacci(number)
    };

    testing_fibonacci(n: Int) : IO {{
        out_string("Iterative Fibonacci : ");
        out_int(iterative_fibonacci(5));
        out_string("\n");

        out_string("Recursive Fibonacci : ");
        out_int(recursive_fibonacci(5));
        out_string("\n");
    }};

    recursive_fibonacci (n: AUTO_TYPE) : AUTO_TYPE {
        if n <= 2 then 1 else recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2) fi
    };

    iterative_fibonacci(n: AUTO_TYPE) : AUTO_TYPE {
        let  i: Int <- 2, n1: Int <- 1, n2: Int <- 1, temp: Int in {
            while i < n loop
                let temp: Int <- n2 in {
                    n2 <- n2 + n1;
                    n1 <- temp;
                    i <- i + 1;
                }
            pool;
            n2;
        }
    };
};
'''

def main(G):
    st.title('Type Inferencer')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    text = st.text_area('Input your code here:')

    if text:
        st.text(text)
        try:
            tokens = list(tokenize_text(text))
        except Exception as e:
            st.error(f'Lexer Error: You probably did something wrong :wink:')
        else:
            try:
                parser = LR1Parser(G)
                parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
            except Exception as e:
                st.error(f'Parser Error: You probably did something wrong :wink:')
            else:
                ast = evaluate_reverse_parse(parse, operations, tokens)

                st.title('Results:')
                
                errors = []
                collector = TypeCollector(errors)
                collector.visit(ast)
                context = collector.context

                # for e in errors:
                    # st.error(e)
                # st.text('Context:')
                # st.text(context)

                # st.subheader('Building types')
                builder = TypeBuilder(context, errors)
                builder.visit(ast)
                manager = builder.manager
                # for e in errors:
                    # st.error(e)
                # st.text('Context:')
                # st.text(context)

                # st.subheader('Checking types')
                checker = TypeChecker(context, manager, [])
                scope = checker.visit(ast)

                # st.subheader('Infering types')
                temp_errors = []
                inferencer = TypeInferencer(context, manager, temp_errors)
                inferencer.visit(ast, scope)
                # for e in temp_errors:
                #     st.error(e)

                # st.subheader('Last check')
                errors.extend(temp_errors)
                checker = TypeChecker(context, manager, errors)
                checker.visit(ast)
                for e in errors:
                    st.error(e)
                    
                formatter = FormatVisitor()
                tree = formatter.visit(ast)
                st.text(tree)

if __name__ == '__main__':
    # main(G)
    ast = run_pipeline(G, text)