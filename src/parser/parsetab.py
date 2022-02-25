
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftATleftINT_COMPLEMENTleftISVOIDleftNOTleftLESSEQUALLESSEQUALleftPLUSMINUSleftMULTDIVleftDOTACTION ASSIGN AT BOOL CASE CBRACE CLASS COLON COMMA CPAR DIV DOT ELSE EQUAL ESAC FI ID IF IN INHERITS INTEGER INT_COMPLEMENT ISVOID LESS LESSEQUAL LET LOOP MINUS MULT NEW NOT OBRACE OF OPAR PLUS POOL SEMICOLON STRING THEN TYPE WHILEprogram : class_listepsilon :class_list : def_class SEMICOLON class_list\n                  | def_class SEMICOLONdef_class : CLASS TYPE OBRACE feature_list CBRACE\n                 | CLASS TYPE INHERITS TYPE OBRACE feature_list CBRACEfeature_list : def_attr SEMICOLON feature_list\n                    | def_func SEMICOLON feature_list\n                    | epsilonblock_list : expr SEMICOLON block_list\n                  | expr SEMICOLONdef_attr : ID COLON TYPE ASSIGN expr\n                | ID COLON TYPEdef_func : ID OPAR params CPAR COLON TYPE OBRACE expr CBRACEparams : param_listparams : epsilonparam_list : param COMMA param_list\n                  | param epsilonparam : ID COLON TYPEexpr : LET let_attrs IN expr\n            | CASE expr OF case_list ESAC\n            | IF expr THEN expr ELSE expr FI\n            | WHILE expr LOOP expr POOLexpr : ID ASSIGN exprexpr : expr AT TYPE DOT ID OPAR arg_list CPAR\n            | expr DOT ID OPAR arg_list CPAR\n            | ID OPAR arg_list CPARexpr : expr PLUS expr\n            | expr MINUS expr\n            | expr MULT expr\n            | expr DIV expr\n            | expr LESS expr\n            | expr LESSEQUAL expr\n            | expr EQUAL exprexpr : INT_COMPLEMENT expr\n            | ISVOID expr\n            | NOT exprexpr : OPAR expr CPARexpr : atomlet_attrs : def_attr COMMA let_attrs\n                | def_attrcase_list : case_elem SEMICOLON case_list\n                 | case_elem SEMICOLONcase_elem : ID COLON TYPE ACTION exprarg_list : arg_list_ne\n                | epsilonarg_list_ne : expr COMMA arg_list_ne\n                   | expr atom : IDatom : NEW TYPEatom : blockatom : INTEGERatom :  BOOLatom : STRINGblock : OBRACE block_list CBRACE'
    
_lr_action_items = {'CLASS':([0,5,],[4,4,]),'$end':([1,2,5,7,],[0,-1,-4,-3,]),'SEMICOLON':([3,11,12,16,24,36,37,38,47,49,50,51,52,75,76,77,78,80,82,89,90,91,92,93,94,95,101,102,105,109,112,121,125,126,128,134,135,136,],[5,17,18,-5,-13,-6,-49,-12,-39,-51,-52,-53,-54,-35,-36,-37,-50,103,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,122,-21,-23,-14,-26,-22,-25,-44,]),'TYPE':([4,9,19,32,48,55,59,123,],[6,15,24,54,78,81,87,130,]),'OBRACE':([6,15,31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,81,96,99,100,103,104,106,108,124,127,133,],[8,21,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,104,53,53,53,53,53,53,53,53,53,53,]),'INHERITS':([6,],[9,]),'ID':([8,17,18,20,21,31,34,39,40,41,42,43,44,45,46,53,57,58,60,61,62,63,64,65,66,67,96,97,98,99,100,103,104,106,107,108,122,124,127,133,],[14,14,14,25,14,37,25,70,37,37,37,37,37,37,37,37,37,37,88,37,37,37,37,37,37,37,37,70,113,37,37,37,37,37,119,37,113,37,37,37,]),'CBRACE':([8,10,13,17,18,21,22,23,30,37,47,49,50,51,52,75,76,77,78,79,82,89,90,91,92,93,94,95,101,102,103,105,109,116,117,121,125,128,134,135,],[-2,16,-9,-2,-2,-2,-7,-8,36,-49,-39,-51,-52,-53,-54,-35,-36,-37,-50,102,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-11,-27,-20,-10,126,-21,-23,-26,-22,-25,]),'COLON':([14,25,33,70,113,],[19,32,55,19,123,]),'OPAR':([14,31,37,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,88,96,99,100,103,104,106,108,119,124,127,133,],[20,43,58,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,108,43,43,43,43,43,43,43,127,43,43,43,]),'CPAR':([20,26,27,28,29,35,37,47,49,50,51,52,54,56,58,74,75,76,77,78,82,83,84,85,86,89,90,91,92,93,94,95,101,102,105,108,109,118,120,121,125,127,128,132,134,135,],[-2,33,-15,-16,-2,-18,-49,-39,-51,-52,-53,-54,-19,-17,-2,101,-35,-36,-37,-50,-24,105,-45,-46,-48,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-2,-20,-47,128,-21,-23,-2,-26,135,-22,-25,]),'ASSIGN':([24,37,],[31,57,]),'COMMA':([24,29,37,38,47,49,50,51,52,54,69,75,76,77,78,82,86,89,90,91,92,93,94,95,101,102,105,109,121,125,128,134,135,],[-13,34,-49,-12,-39,-51,-52,-53,-54,-19,97,-35,-36,-37,-50,-24,106,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,-21,-23,-26,-22,-25,]),'IN':([24,37,38,47,49,50,51,52,68,69,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,110,121,125,128,134,135,],[-13,-49,-12,-39,-51,-52,-53,-54,96,-41,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,-40,-21,-23,-26,-22,-25,]),'LET':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'CASE':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'IF':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'WHILE':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'INT_COMPLEMENT':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'ISVOID':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'NOT':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'NEW':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'INTEGER':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'BOOL':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'STRING':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'AT':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,59,-39,-51,-52,-53,-54,59,59,59,59,-35,-36,-37,-50,59,59,59,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,59,59,59,59,-21,-23,-26,59,-22,-25,59,]),'DOT':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,87,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,60,-39,-51,-52,-53,-54,60,60,60,60,60,60,60,-50,60,60,60,107,60,60,60,60,60,60,60,-38,-55,-27,60,60,60,60,-21,-23,-26,60,-22,-25,60,]),'PLUS':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,61,-39,-51,-52,-53,-54,61,61,61,61,61,61,61,-50,61,61,61,-28,-29,-30,-31,61,61,61,-38,-55,-27,61,61,61,61,-21,-23,-26,61,-22,-25,61,]),'MINUS':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,62,-39,-51,-52,-53,-54,62,62,62,62,62,62,62,-50,62,62,62,-28,-29,-30,-31,62,62,62,-38,-55,-27,62,62,62,62,-21,-23,-26,62,-22,-25,62,]),'MULT':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,63,-39,-51,-52,-53,-54,63,63,63,63,63,63,63,-50,63,63,63,63,63,-30,-31,63,63,63,-38,-55,-27,63,63,63,63,-21,-23,-26,63,-22,-25,63,]),'DIV':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,64,-39,-51,-52,-53,-54,64,64,64,64,64,64,64,-50,64,64,64,64,64,-30,-31,64,64,64,-38,-55,-27,64,64,64,64,-21,-23,-26,64,-22,-25,64,]),'LESS':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,65,-39,-51,-52,-53,-54,65,65,65,65,65,65,65,-50,65,65,65,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,65,65,65,65,-21,-23,-26,65,-22,-25,65,]),'LESSEQUAL':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,66,-39,-51,-52,-53,-54,66,66,66,66,66,66,66,-50,66,66,66,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,66,66,66,66,-21,-23,-26,66,-22,-25,66,]),'EQUAL':([37,38,47,49,50,51,52,71,72,73,74,75,76,77,78,80,82,86,89,90,91,92,93,94,95,101,102,105,109,114,115,117,121,125,128,131,134,135,136,],[-49,67,-39,-51,-52,-53,-54,67,67,67,67,67,67,67,-50,67,67,67,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,67,67,67,67,-21,-23,-26,67,-22,-25,67,]),'OF':([37,47,49,50,51,52,71,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,121,125,128,134,135,],[-49,-39,-51,-52,-53,-54,98,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,-21,-23,-26,-22,-25,]),'THEN':([37,47,49,50,51,52,72,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,121,125,128,134,135,],[-49,-39,-51,-52,-53,-54,99,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,-21,-23,-26,-22,-25,]),'LOOP':([37,47,49,50,51,52,73,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,121,125,128,134,135,],[-49,-39,-51,-52,-53,-54,100,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,-21,-23,-26,-22,-25,]),'ELSE':([37,47,49,50,51,52,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,114,121,125,128,134,135,],[-49,-39,-51,-52,-53,-54,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,124,-21,-23,-26,-22,-25,]),'POOL':([37,47,49,50,51,52,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,115,121,125,128,134,135,],[-49,-39,-51,-52,-53,-54,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,125,-21,-23,-26,-22,-25,]),'FI':([37,47,49,50,51,52,75,76,77,78,82,89,90,91,92,93,94,95,101,102,105,109,121,125,128,131,134,135,],[-49,-39,-51,-52,-53,-54,-35,-36,-37,-50,-24,-28,-29,-30,-31,-32,-33,-34,-38,-55,-27,-20,-21,-23,-26,134,-22,-25,]),'ESAC':([111,122,129,],[121,-43,-42,]),'ACTION':([130,],[133,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,5,],[2,7,]),'def_class':([0,5,],[3,3,]),'feature_list':([8,17,18,21,],[10,22,23,30,]),'def_attr':([8,17,18,21,39,97,],[11,11,11,11,69,69,]),'def_func':([8,17,18,21,],[12,12,12,12,]),'epsilon':([8,17,18,20,21,29,58,108,127,],[13,13,13,28,13,35,85,85,85,]),'params':([20,],[26,]),'param_list':([20,34,],[27,56,]),'param':([20,34,],[29,29,]),'expr':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[38,71,72,73,74,75,76,77,80,82,86,89,90,91,92,93,94,95,109,114,115,80,117,86,86,131,86,136,]),'atom':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'block':([31,40,41,42,43,44,45,46,53,57,58,61,62,63,64,65,66,67,96,99,100,103,104,106,108,124,127,133,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'let_attrs':([39,97,],[68,110,]),'block_list':([53,103,],[79,116,]),'arg_list':([58,108,127,],[83,120,132,]),'arg_list_ne':([58,106,108,127,],[84,118,84,84,]),'case_list':([98,122,],[111,129,]),'case_elem':([98,122,],[112,112,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','parser.py',21),
  ('epsilon -> <empty>','epsilon',0,'p_epsilon','parser.py',26),
  ('class_list -> def_class SEMICOLON class_list','class_list',3,'p_class_list','parser.py',31),
  ('class_list -> def_class SEMICOLON','class_list',2,'p_class_list','parser.py',32),
  ('def_class -> CLASS TYPE OBRACE feature_list CBRACE','def_class',5,'p_def_class','parser.py',41),
  ('def_class -> CLASS TYPE INHERITS TYPE OBRACE feature_list CBRACE','def_class',7,'p_def_class','parser.py',42),
  ('feature_list -> def_attr SEMICOLON feature_list','feature_list',3,'p_feature_list','parser.py',51),
  ('feature_list -> def_func SEMICOLON feature_list','feature_list',3,'p_feature_list','parser.py',52),
  ('feature_list -> epsilon','feature_list',1,'p_feature_list','parser.py',53),
  ('block_list -> expr SEMICOLON block_list','block_list',3,'p_block_list','parser.py',61),
  ('block_list -> expr SEMICOLON','block_list',2,'p_block_list','parser.py',62),
  ('def_attr -> ID COLON TYPE ASSIGN expr','def_attr',5,'p_def_attr_declaration','parser.py',67),
  ('def_attr -> ID COLON TYPE','def_attr',3,'p_def_attr_declaration','parser.py',68),
  ('def_func -> ID OPAR params CPAR COLON TYPE OBRACE expr CBRACE','def_func',9,'p_def_func','parser.py',76),
  ('params -> param_list','params',1,'p_params_ne','parser.py',81),
  ('params -> epsilon','params',1,'p_params_e','parser.py',86),
  ('param_list -> param COMMA param_list','param_list',3,'p_param_list','parser.py',91),
  ('param_list -> param epsilon','param_list',2,'p_param_list','parser.py',92),
  ('param -> ID COLON TYPE','param',3,'p_param','parser.py',100),
  ('expr -> LET let_attrs IN expr','expr',4,'p_expr_flow','parser.py',106),
  ('expr -> CASE expr OF case_list ESAC','expr',5,'p_expr_flow','parser.py',107),
  ('expr -> IF expr THEN expr ELSE expr FI','expr',7,'p_expr_flow','parser.py',108),
  ('expr -> WHILE expr LOOP expr POOL','expr',5,'p_expr_flow','parser.py',109),
  ('expr -> ID ASSIGN expr','expr',3,'p_expr_assign','parser.py',123),
  ('expr -> expr AT TYPE DOT ID OPAR arg_list CPAR','expr',8,'p_expr_func_all','parser.py',128),
  ('expr -> expr DOT ID OPAR arg_list CPAR','expr',6,'p_expr_func_all','parser.py',129),
  ('expr -> ID OPAR arg_list CPAR','expr',4,'p_expr_func_all','parser.py',130),
  ('expr -> expr PLUS expr','expr',3,'p_expr_operators_binary','parser.py',148),
  ('expr -> expr MINUS expr','expr',3,'p_expr_operators_binary','parser.py',149),
  ('expr -> expr MULT expr','expr',3,'p_expr_operators_binary','parser.py',150),
  ('expr -> expr DIV expr','expr',3,'p_expr_operators_binary','parser.py',151),
  ('expr -> expr LESS expr','expr',3,'p_expr_operators_binary','parser.py',152),
  ('expr -> expr LESSEQUAL expr','expr',3,'p_expr_operators_binary','parser.py',153),
  ('expr -> expr EQUAL expr','expr',3,'p_expr_operators_binary','parser.py',154),
  ('expr -> INT_COMPLEMENT expr','expr',2,'p_expr_operators_unary','parser.py',173),
  ('expr -> ISVOID expr','expr',2,'p_expr_operators_unary','parser.py',174),
  ('expr -> NOT expr','expr',2,'p_expr_operators_unary','parser.py',175),
  ('expr -> OPAR expr CPAR','expr',3,'p_expr_group','parser.py',186),
  ('expr -> atom','expr',1,'p_expr_atom','parser.py',191),
  ('let_attrs -> def_attr COMMA let_attrs','let_attrs',3,'p_let_attrs','parser.py',196),
  ('let_attrs -> def_attr','let_attrs',1,'p_let_attrs','parser.py',197),
  ('case_list -> case_elem SEMICOLON case_list','case_list',3,'p_case_list','parser.py',205),
  ('case_list -> case_elem SEMICOLON','case_list',2,'p_case_list','parser.py',206),
  ('case_elem -> ID COLON TYPE ACTION expr','case_elem',5,'p_case_elem','parser.py',214),
  ('arg_list -> arg_list_ne','arg_list',1,'p_arg_list','parser.py',219),
  ('arg_list -> epsilon','arg_list',1,'p_arg_list','parser.py',220),
  ('arg_list_ne -> expr COMMA arg_list_ne','arg_list_ne',3,'p_arg_list_ne','parser.py',225),
  ('arg_list_ne -> expr','arg_list_ne',1,'p_arg_list_ne','parser.py',226),
  ('atom -> ID','atom',1,'p_atom_id','parser.py',234),
  ('atom -> NEW TYPE','atom',2,'p_atom_new','parser.py',239),
  ('atom -> block','atom',1,'p_atom_block','parser.py',244),
  ('atom -> INTEGER','atom',1,'p_atom_int','parser.py',249),
  ('atom -> BOOL','atom',1,'p_atom_bool','parser.py',254),
  ('atom -> STRING','atom',1,'p_atom_atring','parser.py',259),
  ('block -> OBRACE block_list CBRACE','block',3,'p_block','parser.py',264),
]
