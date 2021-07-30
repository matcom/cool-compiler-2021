import os
import streamlit as st
from Serializer import Serializer
from Grammar import pprint_tokens
from TypeCollector import TypeCollector
from TypeBuilder import TypeBuilder
from TypeChecker import TypeChecker
from TypeInferencer import TypeInferencer
from Utils import AnalizeScopeAutoTypes, AnalizeClassAutoTypes
from cmp.evaluation import evaluate_reverse_parse

st.title('Welcome to the Cool Interpreter ! 👋')
text = st.text_area('Introduce the code to analize')
if st.button('Run') and text:
    
    st.subheader('Text:')
    st.text(text)

    try:
        # Tokenizer
        lexer = Serializer.load(os.getcwd() + '/lexer')
        tokens = lexer.get_tokens(text)
        # pprint_tokens(tokens)

        try:
            # Parser
            parser = Serializer.load(os.getcwd() + '/parser')
            parse, operations = parser([t.token_type.Name for t in tokens])
            ast = evaluate_reverse_parse(parse, operations, tokens)

            # Collecting Types
            collector = TypeCollector()
            collector.visit(ast)
            context = collector.context
            errors = collector.errors

            # Building Types
            builder = TypeBuilder(context, errors)
            builder.visit(ast)

            # Checking Types
            checker = TypeChecker(context, errors)
            scope = checker.visit(ast)

            # Infering Types
            while True:
                inferencer = TypeInferencer(context, errors)
                if not inferencer.visit(ast):
                    break

            inferences = []
            for declaration in ast.declarations:
                AnalizeClassAutoTypes(context.get_type(declaration.id), errors, inferences)
            AnalizeScopeAutoTypes(scope, errors, inferences)

            # Print Inferences
            st.subheader("Infered Types:")
            if inferences:
                for inf in inferences:
                    st.warning(inf)
            else:
                st.text("There wasn't any variable type infered.")

            # Print Errors
            st.subheader("Errors:")
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.text("There wasn't any error in the code entered.")

        except:
            st.error("The text entered doesn't belong to COOL Language.")       

    except: 
        st.error("The text has characters that don't belong to COOL Language.")    
