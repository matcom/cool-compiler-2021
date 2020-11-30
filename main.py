from src.lexical_analizer import tokenize_cool_text
from src.cool_grammar import define_cool_grammar
from src.cool_visitor import FormatVisitorST

from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger

from src.shift_reduce_parsers import LR1Parser, DerivationTree
from src.errors import parsing_table_error, Error

from src.cmp.evaluation import evaluate_reverse_parse

import streamlit as st
from src.ui import print_array, print_grammar, print_tset

st.sidebar.header("About")
st.sidebar.subheader("Segundo Proyecto de Compilacion: Cool Intrepreter")
st.sidebar.text("Amalia Ibarra Rodriguez")
st.sidebar.text("Gabriela B. Martinez Giraldo")
st.sidebar.text("Grupo: C-312")
st.sidebar.text("Curso: 2019-2020")

""" # Cool Intrepreter """

data = st.text_area("Type some code", "")
run_analysis = st.button("compile", "")


initial_ast = "Initial_AST"
final_ast = "Final_AST"
reduced_sets = "ReducedSets"


selected_options = st.multiselect(
    "Select what to see", (initial_ast, final_ast, reduced_sets),
)


def run_pipeline(text):
    # define grammar
    grammar, idx, string, num = define_cool_grammar()

    try:
        tokens = tokenize_cool_text(grammar, idx, string, num, text)

        parser = LR1Parser(grammar)
        parse, operations = parser([t.token_type for t in tokens])

        # print("\n".join(repr(x) for x in parse))
        # print(operations)

        ast = evaluate_reverse_parse(parse, operations, tokens)
        formatter = FormatVisitorST()
        tree = formatter.visit(ast)

        if initial_ast in selected_options:
            st.header("Initial Tree:")
            print_array(tree)

        errors = []

        collector = TypeCollector(errors)
        collector.visit(ast)

        context = collector.context

        builder = TypeBuilder(context, errors)
        builder.visit(ast)

        checker = TypeChecker(context, errors)
        checker.visit(ast, None)

        if errors != []:
            st.header("Sorry we found some errors in your code:")
            print_array(errors)
        else:
            tset_builder = TSetBuilder(context, errors)
            tset = tset_builder.visit(ast, None)

            tset_reducer = TSetReducer(context, errors)
            reduced_set = tset_reducer.visit(ast, tset)

            tset_merger = TSetMerger(context, errors)
            tset_merger.visit(ast, reduced_set)

            collector = TypeCollector(errors)
            collector.visit(ast)

            context = collector.context

            builder = TypeBuilder(context, errors)
            builder.visit(ast)

            checker = TypeChecker(context, errors)
            checker.visit(ast, None)

            if reduced_sets in selected_options:
                st.header("Reduced Sets")
                print_tset(reduced_set)

            if final_ast in selected_options:
                tree = formatter.visit(ast)
                st.header("Final Tree:")
                print_array(tree)

    except Error as error:
        st.header("Sorry an error occur while tokenizing text:")
        st.write(str(error))


if run_analysis:
    run_pipeline(data)

