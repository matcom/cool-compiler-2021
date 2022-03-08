import os
from grammar_class import Grammar
import ast_cool_hierarchy as ast
import ast_cool_h_extender as to_ast



def attr_decoder(attr, symbols_to_reduce, ast_class):
    def get_line_col(args:list):
        i=0
        l=len(args)
        while i<l:
            term=args[i]
            if hasattr(term,"line_no") and term.line_no !=-1:
                return term.line_no, term.col_no
            i+=1
        return -1,-1

    if attr:
        if len(attr)==2:
            attr_class, attr_pos = attr
            symbols_to_reduce.append(None)
            args = list(map(lambda i: symbols_to_reduce[i].tag if symbols_to_reduce[i] is not None else None, attr_pos))
            #line,col=-1
            if len(args)>0 and isinstance(args[0],list) and len(args[0]) and hasattr(args[0][0],"line_no") and args[0][0].line_no!=-1:
                line=args[0][0].line_no
                col=args[0][0].col_no
            else: 
                line,col=get_line_col(args)
            args = list(map(lambda s: s.lexeme if hasattr(s,"lexeme") else s, args))
            args=[line,col,*args]
            classes=ast_class.get(attr_class)
            instanc=classes(*args)
            return instanc
        if len(attr) == 1:
            if isinstance(attr[0], int):
                attr_pos = attr[0]
                return symbols_to_reduce[attr_pos].tag
            elif isinstance(attr[0], str):
                attr_class = attr[0]
                arg = symbols_to_reduce[0].tag if len(symbols_to_reduce) and symbols_to_reduce[0] is not None else None
                if isinstance(arg,list) and len(arg) and hasattr(arg[0],"line_no"):
                    line=arg[0].line_no
                    col=arg[0].col_no
                else: 
                    line=arg.line_no if hasattr(arg,"line_no") else -1
                    col=arg.col_no if hasattr(arg,"col_no") else -1
                arg = arg.lexeme if hasattr(arg,"lexeme") else arg
                classes=ast_class.get(attr_class)
                instanc=classes(line,col,arg)
                return instanc
            else:
                raise Exception("Invalid Attribute")
        else:
            raise Exception("Invalid Attribute")
    return symbols_to_reduce[0].tag if len(symbols_to_reduce) and symbols_to_reduce[0] is not None else None


cool_grammar = Grammar("cool",attr_decoder)

#### TERMINALS ####
#Ignore Tokens \t\r\f
line_break,tab,nxt_page,space=cool_grammar.terminal((to_ast.TOKEN_TYPE.LINEBREAK,'\n|\r',(True,)),
                                                    (to_ast.TOKEN_TYPE.TAB,'\t',(True,)),
                                                    (to_ast.TOKEN_TYPE.NXTPAGE,'\f',(True,)),
                                                    (to_ast.TOKEN_TYPE.SPACE,' ',(True,)))
# Operators / * + -
div, mult, plus, minus = cool_grammar.terminal((to_ast.TOKEN_TYPE.DIV, "\/"),
                                               (to_ast.TOKEN_TYPE.MULT, "\*"),
                                               (to_ast.TOKEN_TYPE.PLUS, "\+"),
                                               (to_ast.TOKEN_TYPE.MINUS, "\-"))
# Comparators & Assigns = < <= <- , => ~
eq, lt, lteq, assign, action, int_comp = cool_grammar.terminal((to_ast.TOKEN_TYPE.EQ, "="),
                                                               (to_ast.TOKEN_TYPE.LT,
                                                                "<"),
                                                               (to_ast.TOKEN_TYPE.LTEQ,
                                                                "<="),
                                                               (to_ast.TOKEN_TYPE.ASSIGN,
                                                                "<\-"),
                                                               (to_ast.TOKEN_TYPE.ACTION,
                                                                "=>"),
                                                               (to_ast.TOKEN_TYPE.INT_COMP, "~"))
# gropers ( ) [ ]
lparen, rparen, lbrace, rbrace = cool_grammar.terminal((to_ast.TOKEN_TYPE.LPAREN, "\("),
                                                       (to_ast.TOKEN_TYPE.RPAREN, "\)"),
                                                       (to_ast.TOKEN_TYPE.LBRACE,
                                                        "{"),
                                                       (to_ast.TOKEN_TYPE.RBRACE, "}"))

# Separators
dot, comma, colon, semicolon = cool_grammar.terminal((to_ast.TOKEN_TYPE.DOT, "\."),
                                                     (to_ast.TOKEN_TYPE.COMMA, ","),
                                                     (to_ast.TOKEN_TYPE.COLON, ":"),
                                                     (to_ast.TOKEN_TYPE.SEMICOLON, ";"))

at = cool_grammar.terminal((to_ast.TOKEN_TYPE.AT, "@"))

class_, inherits, new_, isvoid = cool_grammar.terminal((to_ast.TOKEN_TYPE.CLASS, '[Cc][Ll][Aa][Ss][Ss]'),
                                                       (to_ast.TOKEN_TYPE.INHERITS,
                                                        '[Ii][Nn][Hh][Ee][Rr][Ii][Tt][Ss]'),
                                                       (to_ast.TOKEN_TYPE.NEW, '[Nn][Ee][Ww]'),
                                                       (to_ast.TOKEN_TYPE.ISVOID, '[Ii][Ss][Vv][Oo][Ii][Dd]'))

in_, case, of, esac = cool_grammar.terminal((to_ast.TOKEN_TYPE.IN, '[Ii][Nn]'),
                                            (to_ast.TOKEN_TYPE.CASE, '[Cc][Aa][Ss][Ee]'),
                                            (to_ast.TOKEN_TYPE.OF, '[Oo][Ff]'),
                                            (to_ast.TOKEN_TYPE.ESAC, '[Ee][Ss][Aa][Cc]'))

if_, then, else_, fi = cool_grammar.terminal((to_ast.TOKEN_TYPE.IF, '[Ii][Ff]'),
                                             (to_ast.TOKEN_TYPE.THEN, '[Tt][Hh][Ee][Nn]'),
                                             (to_ast.TOKEN_TYPE.ELSE, '[Ee][Ll][Ss][Ee]'),
                                             (to_ast.TOKEN_TYPE.FI, '[Ff][Ii]'))

while_, loop_, pool = cool_grammar.terminal((to_ast.TOKEN_TYPE.WHILE, '[Ww][Hh][Ii][Ll][Ee]'),
                                            (to_ast.TOKEN_TYPE.LOOP, '[Ll][Oo][Oo][Pp]'),
                                            (to_ast.TOKEN_TYPE.POOL, '[Pp][Oo][Oo][Ll]'))

let, not_ = cool_grammar.terminal((to_ast.TOKEN_TYPE.LET, '[Ll][Ee][Tt]'),
                                  (to_ast.TOKEN_TYPE.NOT, '[Nn][Oo][Tt]'))

# Non-empty strings of digits 0-9
integer = cool_grammar.terminal((to_ast.TOKEN_TYPE.INTEGER, '[0-9]+'))
# booleans
true = cool_grammar.terminal(
    (to_ast.TOKEN_TYPE.TRUE, '[t][Rr][Uu][Ee]',(False,[],'True')))

false= cool_grammar.terminal(
    (to_ast.TOKEN_TYPE.FALSE, '[f][Aa][Ll][Ss][Ee]', (False,[],'False')))

self_type = cool_grammar.terminal((to_ast.TOKEN_TYPE.SELF_TYPE, 'SELF_TYPE'))
# Begin with a capital letter
type_id = cool_grammar.terminal((to_ast.TOKEN_TYPE.TYPE_ID, '[A-Z][a-zA-Z0-9_]*'))

#self_obj = cool_grammar.terminal((to_ast.TOKEN_TYPE.SELF_OBJECT, 'self'))

# Begin with a lower case letter
obj_id = cool_grammar.terminal(
    (to_ast.TOKEN_TYPE.OBJECT_ID, '[a-z][a-zA-Z0-9_]*'))

string = cool_grammar.terminal(
    (to_ast.TOKEN_TYPE.STRING, '"[^\\\\"\n]*((\\\\\r?\n|\\\\.)[^"\\\\\n]*)*"', (False,["\0"])))
    #(to_ast.TOKEN_TYPE.STRING, '"[^\\\\"\0\n]*((\\\\\r?\n|\\\\.)[^"\\\\\0\n]*)*"'))

line_comment = cool_grammar.terminal(
    (to_ast.TOKEN_TYPE.LINECOMMENT, '\\-\\-[^\r\n]*\r?\n', (True,)))

multiline_comment = cool_grammar.terminal(
    (to_ast.TOKEN_TYPE.MULTILINECOMMENT,r'(\(\*)(([^\*]*)(\*[^\)\*])?)*(\*+\))', (True,)))


### NON TERMINALS ####

Program, Class_list, Class_def, Feature_list, Meth_def, Attrs_def, Attr_def=\
    cool_grammar.nonTerminals(*"Program,Class_list,Class_def,Feature_list,Meth_def,"
                               "Attrs_def,Attr_def".split(","))
Type, Expr, Param_list, Param, Other_param, Comparer, Open_expr_lvl1=\
    cool_grammar.nonTerminals(*"Type,Expr,Param_list,Param,Other_param,Comparer,Open_expr_lvl1".split(","))

Arith, Open_expr_lvl2, Term, Open_expr_lvl3, Open_expr, Let_var_list=\
    cool_grammar.nonTerminals(*"Arith,Open_expr_lvl2,Term,Open_expr_lvl3,Open_expr,Let_var_list".split(","))

Let_var , Let_var_assign , Branch , Factor, Atom, Bool=\
    cool_grammar.nonTerminals(*"Let_var,Let_var_assign,Branch,Factor,Atom,Bool".split(","))

Open_Expr, Expr_list, Branch_list, Func_call, Arg_list, Other_arg =\
    cool_grammar.nonTerminals(*"Open_Expr,Expr_list,Branch_list,Func_call,Arg_list,Other_arg".split(","))

Resoluted =cool_grammar.nonTerminals("Resoluted")

# Productions
Program != Class_list / (ast.ProgramNode, )

Class_list != Class_def / (to_ast.ListNode,) \
    | Class_def + Class_list /(to_ast.ListNode, (0,1))

Class_def != class_ + type_id + lbrace + Feature_list + rbrace + semicolon / (to_ast.ClassDeclarationWrapper,( 1, 3)) \
    | class_ + type_id + inherits + type_id + lbrace + Feature_list + rbrace + semicolon / (ast.ClassDeclarationNode,( 1, 5, 3))

Feature_list != Attrs_def + semicolon + Feature_list  / (to_ast.ListNode,(0,2))\
    | Meth_def + semicolon + Feature_list  / (to_ast.ListNode,(0,2)) \
    | cool_grammar.epsilon /(to_ast.ListNode,)

Attrs_def != Attr_def \
    | Attr_def + comma + Attrs_def  / (to_ast.ListNode,(0,2))

Attr_def != obj_id + colon + Type / (ast.AttrDeclarationNode,( 0, 2)) \
    | obj_id + colon + Type + assign + Expr / (ast.AttrDeclarationNode,(0, 2, 4))

Meth_def != obj_id + lparen + Param_list + rparen + colon + Type + lbrace + \
    Expr + rbrace / (ast.FuncDeclarationNode,(0, 2, 5, 7))

Param_list != Param + Other_param / (to_ast.ListNode,(0,1)) \
    | cool_grammar.epsilon /(to_ast.ListNode,)
 #   | Param /(to_ast.ListNode,) \

Param != obj_id + colon + Type / (to_ast.TupleWrapper,(0,2))

Other_param != comma + Param + Other_param / (to_ast.ListNode,(1,2)) \
    | cool_grammar.epsilon /(to_ast.ListNode,)

Expr != Comparer + lt + Open_expr_lvl1 / (ast.LessNode,( 0, 2)) \
    | Comparer + lteq + Open_expr_lvl1 / (ast.LessEqualNode,( 0, 2)) \
    | Comparer + eq + Open_expr_lvl1 / (ast.EqualNode,( 0, 2)) \
    | Open_expr_lvl1 \
    | Comparer

Open_expr_lvl1 != Arith + plus + Open_expr_lvl2 / (ast.PlusNode,( 0, 2)) \
    | Arith + minus + Open_expr_lvl2 / (ast.MinusNode,( 0, 2)) \
    | Open_expr_lvl2

Open_expr_lvl2 != Term + mult + Open_expr_lvl3 / (ast.StarNode,( 0, 2)) \
    | Term + div + Open_expr_lvl3 / (ast.DivNode,( 0, 2)) \
    | Open_expr_lvl3

Open_expr_lvl3 != isvoid + Open_expr_lvl3 / (ast.IsVoidNode,( 1,)) \
    | int_comp + Open_expr_lvl3 / (ast.IntCompNode,( 1,)) \
    | Open_expr

Open_expr != let + Let_var_list + in_ + Expr / (ast.LetNode,( 1, 3)) \
    | obj_id + assign + Expr / (ast.AssignNode,( 0, 2)) \
    | not_ + Expr / (ast.NotNode,( 1,))

Comparer != Comparer + lt + Arith / (ast.LessNode,( 0, 2)) \
    | Comparer + lteq + Arith / (ast.LessEqualNode,( 0, 2)) \
    | Comparer + eq + Arith / (ast.EqualNode,( 0, 2)) \
    | Arith

Arith != Arith + plus + Term / (ast.PlusNode,( 0, 2)) \
    | Arith + minus + Term / (ast.MinusNode,( 0, 2)) \
    | Term

Term != Term + mult + Factor / (ast.StarNode,( 0, 2)) \
    | Term + div + Factor / (ast.DivNode,( 0, 2)) \
    | Factor

Factor != isvoid + Factor / (ast.IsVoidNode,( 1,)) \
    | int_comp + Factor / (ast.IntCompNode,( 1,)) \
    | Resoluted
    #|Atom

Resoluted !=  Resoluted + dot + obj_id + lparen + Arg_list + rparen / (ast.CallNode,( 0, 2, 4)) \
    | Resoluted + at + type_id + dot + obj_id + lparen + Arg_list + rparen / (ast.CallNode,( 0, 4, 6, 2)) \
    | Atom

Atom != integer / (ast.ConstantNumNode, ) \
    | obj_id / (ast.VariableNode, ) \
    | string / (to_ast.StringWrapper, ) \
    | Bool / (ast.BoolNode, ) \
    | lparen + Expr + rparen / (1,) \
    | new_ + type_id / (ast.InstantiateNode,(1,)) \
    | if_ + Expr + then + Expr + else_ + Expr + fi / (ast.ConditionalNode,( 1, 3, 5)) \
    | while_ + Expr + loop_ + Expr + pool / (ast.LoopNode,( 1, 3)) \
    | lbrace + Expr_list + rbrace / (ast.BlockNode,( 1,)) \
    | case + Expr + of + Branch_list + esac / (ast.CaseNode,( 1, 3)) \
    | Func_call 

Expr_list != Expr + semicolon / (to_ast.ListNode,(0,))\
    | Expr + semicolon + Expr_list / (to_ast.ListNode,(0,2))

Let_var_list != Let_var / (to_ast.ListNode,) \
    | Let_var + comma + Let_var_list / (to_ast.ListNode,(0,2)) \
    | Let_var_assign  / (to_ast.ListNode,) \
    | Let_var_assign + comma + Let_var_list / (to_ast.ListNode,(0,2))

Let_var != obj_id + colon + Type / (to_ast.TupleWrapper,(0,2,-1))

Let_var_assign !=  obj_id + colon + Type + assign + Expr / (to_ast.TupleWrapper,(0,2,4))

Branch_list != Branch + Branch_list / (to_ast.ListNode,(0,1)) \
    | Branch / (to_ast.ListNode,)

Branch != obj_id + colon + Type + action + Expr + semicolon / (ast.BranchNode,(0,2,4))

Func_call !=  obj_id + lparen + Arg_list + rparen / (to_ast.CallNodeWrapper,( 0, 2)) 
#    | Atom + dot + obj_id + lparen + Arg_list + rparen / (ast.CallNode,( 0, 2, 4)) \
#    | Atom + at + type_id + dot + obj_id + lparen + Arg_list + rparen / (ast.CallNode,( 0, 4, 6, 2))

Arg_list != Expr + Other_arg / (to_ast.ListNode,(0,1)) \
    | cool_grammar.epsilon /(to_ast.ListNode,)
#    | Expr / (to_ast.ListNode,)\
#    | cool_grammar.epsilon /(to_ast.ListNode,)

Other_arg != comma + Expr + Other_arg / (to_ast.ListNode,(1,2)) \
    | cool_grammar.epsilon /(to_ast.ListNode,)

Type != type_id \
    | self_type

Bool != true | false

current_path = os.path.dirname(__file__)
cool_grammar.parser(current_path)
cool_grammar.lexer(current_path)