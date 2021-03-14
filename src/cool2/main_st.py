import streamlit as st
import time
from cool.parser.cool_parser import save_parser,cool_parser_path, cool_parser
from cool.lexer.cool_lexer import save_lexer,cool_lexer_path, cool_tokens_def
from cool.grammar.cool_grammar import G
from cool.parser.comment_parser import comment_parser_path, comment_parser
from cool.lexer.comment_lexer import comment_lexer_path, comment_tokens_def
from cool.grammar.comment_grammar import C
from cool.visitors.visitors import FormatVisitor
from cool.pipeline import reconstr_pipeline

run_mode = "Correr código"
option_mode = "Opciones"

st.title("Proyecto II de Compilación")

mode = st.sidebar.selectbox("Modos",[run_mode, option_mode])

if mode == run_mode: 
    code = st.text_area("Código")

    if st.button("Correr"):
        result = reconstr_pipeline(code, verbose=True)
        ast, g_errors, parse, tokens, context, scope, operator, value, reconstr_text = [result[x] for x in ["ast", "errors", "text_parse", "text_tokens", "context", "scope", "operator", "value", "reconstructed_text"]] 
        if g_errors:
            st.json(g_errors)
        else:
            st.subheader("Código con AUTO_TYPE inferidos")
            st.text(reconstr_text)
            
            st.subheader("AST")
            format_visitor = FormatVisitor()
            text = format_visitor.visit(ast)
            st.text(text)
            
            parse.reverse()
            parse_str = ""
            for y in [str(x) + "\n" for x in parse]:
                parse_str += y
            st.subheader("Parse")
            st.text(parse_str)
            
            token_str = ""
            for y in [str(x) + "\n" for x in tokens]:
                token_str += y 
            st.subheader("Tokens")
            st.text(token_str)
            st.subheader("Contexto")
            st.text(context)
            st.subheader("Scope")
            st.text(scope)
            st.subheader("Operadores")
            st.text(operator)
            st.subheader("Resultado del programa")
            st.text(value)
            
            

if mode == option_mode:
    if st.checkbox("Ver opciones para actualizar los parsers y lexers"):
        loading = st.empty()
        if st.button("Recrear Parsers"):
            loading.text("Creando el parser de comentarios...")
            obj = save_parser(comment_parser_path,C)
            if obj.errors:
                st.subheader("Errores creando el parser de comentarios")
                st.json(obj.errors)
            
            loading.text("Creando el parser de cool...")
            obj = save_parser(cool_parser_path,G)
            if obj.errors:
                st.subheader("Errores creando el parser de cool")
                st.json(obj.errors)
                
            loading.empty()
            
            
        if st.button("Recrear Lexers"):
            loading.text("Creando el lexer de comentarios...")
            
            obj = save_lexer(comment_tokens_def,comment_lexer_path,C)
            if not obj:
                st.error("Fallo crear el lexer de comentarios")
            
            loading.text("Creando el lexer de cool...")
            obj = save_lexer(cool_tokens_def,cool_lexer_path,G)
            if not obj:
                st.error("Fallo crear el lexer de cool")
                
            loading.empty()
            