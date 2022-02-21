
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programARROW ASSIGN AT BOOL CASE CLASS COLON COMMA DIV DOT ELSE EQUAL ESAC FI ID IF IN INHERITS INT ISVOID LBRACE LESS LESSEQ LET LNOT LOOP LPAREN MINUS NEW NOT OF PLUS POOL RBRACE RPAREN SEMICOLON STAR STRING THEN TYPE WHILEprogram : class_listepsilon :class_list : def_class SEMICOLON class_list\n                      | def_class SEMICOLON def_class : CLASS TYPE LBRACE feature_list RBRACE\n                     | CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACEfeature_list : def_attr SEMICOLON feature_list\n                        | def_func SEMICOLON feature_list\n                        | epsilondef_attr : ID COLON TYPE\n                    | ID COLON TYPE ASSIGN exprdef_func : ID LPAREN params RPAREN COLON TYPE LBRACE expr RBRACEparams : param_list\n                  | param_list_emptyparam_list : param\n                      | param COMMA param_listparam_list_empty : epsilonparam : ID COLON TYPEexpr : LET let_attrs IN expr\n                | CASE expr OF case_list ESAC\n                | IF expr THEN expr ELSE expr FI\n                | WHILE expr LOOP expr POOLexpr : ID ASSIGN exprexpr : expr AT TYPE DOT ID LPAREN args RPAREN\n                | expr DOT ID LPAREN args RPAREN\n                | ID LPAREN args RPARENexpr : expr PLUS expr\n                | expr MINUS expr\n                | expr STAR expr\n                | expr DIV expr\n                | expr LESS expr\n                | expr LESSEQ expr\n                | expr EQUAL exprexpr : NOT expr\n                | ISVOID expr\n                | LNOT exprexpr : LPAREN expr RPARENexpr : atomlet_attrs : def_var\n                     | def_var COMMA let_attrsdef_var : ID COLON TYPE\n                   | ID COLON TYPE ASSIGN exprcase_list : case_option SEMICOLON\n                     | case_option SEMICOLON case_listcase_option : ID COLON TYPE ARROW exprargs : arg_list\n                | arg_list_emptyarg_list : expr\n                    | expr COMMA arg_listarg_list_empty : epsilonatom : INTatom : IDatom : BOOLatom : STRINGatom : NEW TYPEatom : blockblock : LBRACE block_list RBRACE block_list : expr SEMICOLON\n                       | expr SEMICOLON block_list'
    
_lr_action_items = {'CLASS':([0,5,],[4,4,]),'$end':([1,2,5,7,],[0,-1,-4,-3,]),'SEMICOLON':([3,11,12,16,24,36,37,38,47,48,49,50,52,75,76,77,78,80,82,90,91,92,93,94,95,96,103,104,107,111,115,125,129,130,132,139,140,141,],[5,17,18,-5,-10,-6,-52,-11,-38,-51,-53,-54,-56,-34,-35,-36,-55,105,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,126,-20,-22,-12,-25,-21,-24,-45,]),'TYPE':([4,9,19,33,51,55,59,99,127,],[6,15,24,54,78,81,88,113,135,]),'LBRACE':([6,15,32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,81,97,101,102,105,106,108,110,124,128,131,138,],[8,21,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,106,53,53,53,53,53,53,53,53,53,53,53,]),'INHERITS':([6,],[9,]),'ID':([8,17,18,20,21,32,35,39,40,41,42,43,44,45,46,53,57,58,60,61,62,63,64,65,66,67,97,98,100,101,102,105,106,108,109,110,124,126,128,131,138,],[14,14,14,25,14,37,25,70,37,37,37,37,37,37,37,37,37,37,89,37,37,37,37,37,37,37,37,70,116,37,37,37,37,37,122,37,37,116,37,37,37,]),'RBRACE':([8,10,13,17,18,21,22,23,31,37,47,48,49,50,52,75,76,77,78,79,82,90,91,92,93,94,95,96,103,104,105,107,111,119,120,125,129,132,139,140,],[-2,16,-9,-2,-2,-2,-7,-8,36,-52,-38,-51,-53,-54,-56,-34,-35,-36,-55,104,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-58,-26,-19,-59,130,-20,-22,-25,-21,-24,]),'COLON':([14,25,34,70,116,],[19,33,55,99,127,]),'LPAREN':([14,32,37,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,89,97,101,102,105,106,108,110,122,124,128,131,138,],[20,43,58,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,110,43,43,43,43,43,43,43,131,43,43,43,43,]),'RPAREN':([20,26,27,28,29,30,37,47,48,49,50,52,54,56,58,74,75,76,77,78,82,83,84,85,86,87,90,91,92,93,94,95,96,103,104,107,110,111,121,123,125,129,131,132,137,139,140,],[-2,34,-13,-14,-15,-17,-52,-38,-51,-53,-54,-56,-18,-16,-2,103,-34,-35,-36,-55,-23,107,-46,-47,-48,-50,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-2,-19,-49,132,-20,-22,-2,-25,140,-21,-24,]),'ASSIGN':([24,37,113,],[32,57,124,]),'COMMA':([29,37,47,48,49,50,52,54,69,75,76,77,78,82,86,90,91,92,93,94,95,96,103,104,107,111,113,125,129,132,133,139,140,],[35,-52,-38,-51,-53,-54,-56,-18,98,-34,-35,-36,-55,-23,108,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,-41,-20,-22,-25,-42,-21,-24,]),'LET':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'CASE':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'IF':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'WHILE':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'NOT':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'ISVOID':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'LNOT':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'INT':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'BOOL':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'STRING':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'NEW':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'AT':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,59,-38,-51,-53,-54,-56,59,59,59,59,59,59,59,-55,59,59,59,59,59,59,59,59,59,59,-37,-57,-26,59,59,59,59,-20,-22,-25,59,59,-21,-24,59,]),'DOT':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,88,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,60,-38,-51,-53,-54,-56,60,60,60,60,60,60,60,-55,60,60,60,109,60,60,60,60,60,60,60,-37,-57,-26,60,60,60,60,-20,-22,-25,60,60,-21,-24,60,]),'PLUS':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,61,-38,-51,-53,-54,-56,61,61,61,61,61,61,61,-55,61,61,61,61,61,61,61,61,61,61,-37,-57,-26,61,61,61,61,-20,-22,-25,61,61,-21,-24,61,]),'MINUS':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,62,-38,-51,-53,-54,-56,62,62,62,62,62,62,62,-55,62,62,62,62,62,62,62,62,62,62,-37,-57,-26,62,62,62,62,-20,-22,-25,62,62,-21,-24,62,]),'STAR':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,63,-38,-51,-53,-54,-56,63,63,63,63,63,63,63,-55,63,63,63,63,63,63,63,63,63,63,-37,-57,-26,63,63,63,63,-20,-22,-25,63,63,-21,-24,63,]),'DIV':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,64,-38,-51,-53,-54,-56,64,64,64,64,64,64,64,-55,64,64,64,64,64,64,64,64,64,64,-37,-57,-26,64,64,64,64,-20,-22,-25,64,64,-21,-24,64,]),'LESS':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,65,-38,-51,-53,-54,-56,65,65,65,65,65,65,65,-55,65,65,65,65,65,65,65,65,65,65,-37,-57,-26,65,65,65,65,-20,-22,-25,65,65,-21,-24,65,]),'LESSEQ':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,66,-38,-51,-53,-54,-56,66,66,66,66,66,66,66,-55,66,66,66,66,66,66,66,66,66,66,-37,-57,-26,66,66,66,66,-20,-22,-25,66,66,-21,-24,66,]),'EQUAL':([37,38,47,48,49,50,52,71,72,73,74,75,76,77,78,80,82,86,90,91,92,93,94,95,96,103,104,107,111,117,118,120,125,129,132,133,136,139,140,141,],[-52,67,-38,-51,-53,-54,-56,67,67,67,67,67,67,67,-55,67,67,67,67,67,67,67,67,67,67,-37,-57,-26,67,67,67,67,-20,-22,-25,67,67,-21,-24,67,]),'OF':([37,47,48,49,50,52,71,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,125,129,132,139,140,],[-52,-38,-51,-53,-54,-56,100,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,-20,-22,-25,-21,-24,]),'THEN':([37,47,48,49,50,52,72,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,125,129,132,139,140,],[-52,-38,-51,-53,-54,-56,101,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,-20,-22,-25,-21,-24,]),'LOOP':([37,47,48,49,50,52,73,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,125,129,132,139,140,],[-52,-38,-51,-53,-54,-56,102,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,-20,-22,-25,-21,-24,]),'ELSE':([37,47,48,49,50,52,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,117,125,129,132,139,140,],[-52,-38,-51,-53,-54,-56,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,128,-20,-22,-25,-21,-24,]),'POOL':([37,47,48,49,50,52,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,118,125,129,132,139,140,],[-52,-38,-51,-53,-54,-56,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,129,-20,-22,-25,-21,-24,]),'IN':([37,47,48,49,50,52,68,69,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,112,113,125,129,132,133,139,140,],[-52,-38,-51,-53,-54,-56,97,-39,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,-40,-41,-20,-22,-25,-42,-21,-24,]),'FI':([37,47,48,49,50,52,75,76,77,78,82,90,91,92,93,94,95,96,103,104,107,111,125,129,132,136,139,140,],[-52,-38,-51,-53,-54,-56,-34,-35,-36,-55,-23,-27,-28,-29,-30,-31,-32,-33,-37,-57,-26,-19,-20,-22,-25,139,-21,-24,]),'ESAC':([114,126,134,],[125,-43,-44,]),'ARROW':([135,],[138,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,5,],[2,7,]),'def_class':([0,5,],[3,3,]),'feature_list':([8,17,18,21,],[10,22,23,31,]),'def_attr':([8,17,18,21,],[11,11,11,11,]),'def_func':([8,17,18,21,],[12,12,12,12,]),'epsilon':([8,17,18,20,21,58,110,131,],[13,13,13,30,13,87,87,87,]),'params':([20,],[26,]),'param_list':([20,35,],[27,56,]),'param_list_empty':([20,],[28,]),'param':([20,35,],[29,29,]),'expr':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[38,71,72,73,74,75,76,77,80,82,86,90,91,92,93,94,95,96,111,117,118,80,120,86,86,133,136,86,141,]),'atom':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'block':([32,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,97,101,102,105,106,108,110,124,128,131,138,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'let_attrs':([39,98,],[68,112,]),'def_var':([39,98,],[69,69,]),'block_list':([53,105,],[79,119,]),'args':([58,110,131,],[83,123,137,]),'arg_list':([58,108,110,131,],[84,121,84,84,]),'arg_list_empty':([58,110,131,],[85,85,85,]),'case_list':([100,126,],[114,134,]),'case_option':([100,126,],[115,115,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','parser.py',28),
  ('epsilon -> <empty>','epsilon',0,'p_epsilon','parser.py',32),
  ('class_list -> def_class SEMICOLON class_list','class_list',3,'p_class_list','parser.py',36),
  ('class_list -> def_class SEMICOLON','class_list',2,'p_class_list','parser.py',37),
  ('def_class -> CLASS TYPE LBRACE feature_list RBRACE','def_class',5,'p_def_class','parser.py',41),
  ('def_class -> CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE','def_class',7,'p_def_class','parser.py',42),
  ('feature_list -> def_attr SEMICOLON feature_list','feature_list',3,'p_feature_list','parser.py',49),
  ('feature_list -> def_func SEMICOLON feature_list','feature_list',3,'p_feature_list','parser.py',50),
  ('feature_list -> epsilon','feature_list',1,'p_feature_list','parser.py',51),
  ('def_attr -> ID COLON TYPE','def_attr',3,'p_def_attr','parser.py',55),
  ('def_attr -> ID COLON TYPE ASSIGN expr','def_attr',5,'p_def_attr','parser.py',56),
  ('def_func -> ID LPAREN params RPAREN COLON TYPE LBRACE expr RBRACE','def_func',9,'p_def_func','parser.py',63),
  ('params -> param_list','params',1,'p_params','parser.py',67),
  ('params -> param_list_empty','params',1,'p_params','parser.py',68),
  ('param_list -> param','param_list',1,'p_param_list','parser.py',72),
  ('param_list -> param COMMA param_list','param_list',3,'p_param_list','parser.py',73),
  ('param_list_empty -> epsilon','param_list_empty',1,'p_param_list_empty','parser.py',77),
  ('param -> ID COLON TYPE','param',3,'p_param','parser.py',81),
  ('expr -> LET let_attrs IN expr','expr',4,'p_expr_flow','parser.py',85),
  ('expr -> CASE expr OF case_list ESAC','expr',5,'p_expr_flow','parser.py',86),
  ('expr -> IF expr THEN expr ELSE expr FI','expr',7,'p_expr_flow','parser.py',87),
  ('expr -> WHILE expr LOOP expr POOL','expr',5,'p_expr_flow','parser.py',88),
  ('expr -> ID ASSIGN expr','expr',3,'p_expr_assign','parser.py',100),
  ('expr -> expr AT TYPE DOT ID LPAREN args RPAREN','expr',8,'p_expr_func_call','parser.py',104),
  ('expr -> expr DOT ID LPAREN args RPAREN','expr',6,'p_expr_func_call','parser.py',105),
  ('expr -> ID LPAREN args RPAREN','expr',4,'p_expr_func_call','parser.py',106),
  ('expr -> expr PLUS expr','expr',3,'p_expr_operators_binary','parser.py',123),
  ('expr -> expr MINUS expr','expr',3,'p_expr_operators_binary','parser.py',124),
  ('expr -> expr STAR expr','expr',3,'p_expr_operators_binary','parser.py',125),
  ('expr -> expr DIV expr','expr',3,'p_expr_operators_binary','parser.py',126),
  ('expr -> expr LESS expr','expr',3,'p_expr_operators_binary','parser.py',127),
  ('expr -> expr LESSEQ expr','expr',3,'p_expr_operators_binary','parser.py',128),
  ('expr -> expr EQUAL expr','expr',3,'p_expr_operators_binary','parser.py',129),
  ('expr -> NOT expr','expr',2,'p_expr_operators_unary','parser.py',146),
  ('expr -> ISVOID expr','expr',2,'p_expr_operators_unary','parser.py',147),
  ('expr -> LNOT expr','expr',2,'p_expr_operators_unary','parser.py',148),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expr_group','parser.py',157),
  ('expr -> atom','expr',1,'p_expr_atom','parser.py',161),
  ('let_attrs -> def_var','let_attrs',1,'p_let_attrs','parser.py',165),
  ('let_attrs -> def_var COMMA let_attrs','let_attrs',3,'p_let_attrs','parser.py',166),
  ('def_var -> ID COLON TYPE','def_var',3,'p_def_var','parser.py',170),
  ('def_var -> ID COLON TYPE ASSIGN expr','def_var',5,'p_def_var','parser.py',171),
  ('case_list -> case_option SEMICOLON','case_list',2,'p_case_list','parser.py',178),
  ('case_list -> case_option SEMICOLON case_list','case_list',3,'p_case_list','parser.py',179),
  ('case_option -> ID COLON TYPE ARROW expr','case_option',5,'p_case_option','parser.py',183),
  ('args -> arg_list','args',1,'p_args','parser.py',187),
  ('args -> arg_list_empty','args',1,'p_args','parser.py',188),
  ('arg_list -> expr','arg_list',1,'p_arg_list','parser.py',192),
  ('arg_list -> expr COMMA arg_list','arg_list',3,'p_arg_list','parser.py',193),
  ('arg_list_empty -> epsilon','arg_list_empty',1,'p_arg_list_empty','parser.py',197),
  ('atom -> INT','atom',1,'p_atom_int','parser.py',201),
  ('atom -> ID','atom',1,'p_atom_id','parser.py',205),
  ('atom -> BOOL','atom',1,'p_atom_bool','parser.py',209),
  ('atom -> STRING','atom',1,'p_atom_string','parser.py',213),
  ('atom -> NEW TYPE','atom',2,'p_atom_new','parser.py',217),
  ('atom -> block','atom',1,'p_atom_block','parser.py',221),
  ('block -> LBRACE block_list RBRACE','block',3,'p_block','parser.py',225),
  ('block_list -> expr SEMICOLON','block_list',2,'p_block_list','parser.py',229),
  ('block_list -> expr SEMICOLON block_list','block_list',3,'p_block_list','parser.py',230),
]
