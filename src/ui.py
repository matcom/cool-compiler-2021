from src.cmp.pycompiler import (
    Symbol,
    NonTerminal,
    Terminal,
    EOF,
    Sentence,
    SentenceList,
    Epsilon,
    Production,
    Grammar,
)
import graphviz
import streamlit as st
from pandas import DataFrame
from src.shift_reduce_parsers import ShiftReduceParser


def print_array(array):
    for item in array:
        st.write(item)


def print_tset(tset):
    output = []

    for key, value in tset.locals.items():
        # output.append("\_" + str(key) + ":" + str(value) + "\n")
        # output.append(f"\\__ {key} : {value} aaa")

        st.write("\\__" + str(key) + ":" + str(value))
    for key, child in tset.children.items():
        # output += "\n"
        try:
            # output.append(key.id + "--->")
            # output.append(f"{key.id}---> eee")
            st.write(key.id + "--->")
        except AttributeError:
            # output.append("let or case --->iii")
            st.write("let or case --->")
        # output += "\n"
        # output.append(str(chil))
        # output.append(f"{print_tset(child)} ooo")
        print_tset(child)

        # st.write(str(chil))
    # for item in output:
    #     st.write(item)


def print_grammar(G):
    st.subheader("Simbolo distinguido")
    st.write(G.startSymbol.Name)

    st.subheader("Terminales")
    for t in G.terminals:
        st.write(t.Name)

    st.subheader("No Terminales")
    for nt in G.nonTerminals:
        st.write(nt.Name)

    st.subheader("Producciones")
    for p in G.Productions:
        st.write(p.__repr__())


def table_to_dataframe_ll(table):
    d = {}
    for (state, symbol), value in table.items():
        # value = encode_value(value)
        try:
            d[state][symbol] = value.__repr__()
        except KeyError:
            d[state] = {symbol: value.__repr__()}

    return DataFrame.from_dict(d, orient="index", dtype=str)


def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return "S" + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action == ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value


def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = encode_value(value)
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = {symbol: value}

    return DataFrame.from_dict(d, orient="index", dtype=str)


# def print_automaton(nfa):
#     graph = graphviz.Digraph()

#     if nfa.start not in nfa.finals:
#         graph.attr("node", shape="diamond")
#         graph.node(str(nfa.start))

#     graph.attr("node", shape="doublecircle")
#     for f in nfa.finals:
#         graph.node(str(f))

#     graph.attr("node", shape="circle")
#     for (start, tran), destination in nfa.map.items():
#         tran = "e" if tran == "" else tran
#         for state in destination:
#             if tran == "%" or tran == "none":
#                 continue
#             graph.edge(
#                 str(start), str(state), label=tran,
#             )

#     st.graphviz_chart(graph)
