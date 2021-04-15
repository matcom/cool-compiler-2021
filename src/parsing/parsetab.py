
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "rightASSIGNrightNOTnonassocLESSEQ<=left+-left*/rightISVOIDleft~left@left.ASSIGN CASE CLASS COMMENT ELSE ESAC FALSE FI ID IF IN INHERITS INT ISVOID LESSEQ LET LOOP NEW NOT OF POOL RET STRING THEN TRUE TYPE WHILEprogram : class_listclass_list : class ';' class_list\n    | class ';'class : CLASS TYPE INHERITS TYPE '{' feature_list '}'\n    | CLASS TYPE '{' feature_list '}'feature_list : attribute ';' feature_list\n    | method ';' feature_list\n    | emptyattribute : ID ':' TYPE ASSIGN expression\n    | ID ':' TYPEmethod : ID '(' params_list ')' ':' TYPE '{' expression '}'params_list : param ',' params_list\n    | paramparams_list : emptyparam : ID ':' TYPEexpression_list : expression ';' expression_list\n    | expression ';'expression : ID ASSIGN expressionexpression : IF expression THEN expression ELSE expression FIexpression : WHILE expression LOOP expression POOLexpression : '{' expression_list '}'expression : LET let_list IN expressionlet_list : let_single ',' let_list\n    | let_singlelet_single : ID ':' TYPE ASSIGN expression\n    | ID ':' TYPEexpression : CASE expression OF case_list ESACcase_list : case_single case_list\n    | case_singlecase_single : ID ':' TYPE RET expression ';'expression : expression '@' TYPE '.' ID '(' args_list ')'\n    | expression '.' ID '(' args_list ')'\n    | ID '(' args_list ')'args_list : expression ',' args_list\n    | expressionargs_list : emptyexpression : NEW TYPEexpression : ISVOID expressionexpression : NOT expressionexpression : '~' expressionexpression : expression '+' expressionexpression : expression '-' expressionexpression : expression '/' expressionexpression : expression '*' expressionexpression : expression '<' expressionexpression : expression LESSEQ expressionexpression : expression '=' expressionexpression : '(' expression ')'expression : STRINGexpression : IDexpression : TRUEexpression : FALSEexpression : INTempty : "
    
_lr_action_items = {'CLASS':([0,5,],[4,4,]),'$end':([1,2,5,7,],[0,-1,-3,-2,]),';':([3,12,13,17,25,30,35,36,47,48,49,50,68,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,109,120,122,125,127,132,134,135,],[5,18,19,-5,-10,-4,-50,-9,-49,-51,-52,-53,95,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-20,-27,-11,-32,-19,-31,136,]),'TYPE':([4,8,20,32,43,52,56,98,124,],[6,10,25,51,74,78,83,111,130,]),'INHERITS':([6,],[8,]),'{':([6,10,31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,78,92,93,95,96,101,103,105,119,121,126,133,],[9,16,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,101,39,39,39,39,39,39,39,39,39,39,39,]),'ID':([9,16,18,19,21,31,34,37,38,39,40,41,42,44,45,46,54,55,57,58,59,60,61,62,63,64,92,93,95,96,97,99,101,103,104,105,113,119,121,126,133,136,],[15,15,15,15,26,35,26,35,35,35,71,35,35,35,35,35,35,35,84,35,35,35,35,35,35,35,35,35,35,35,71,114,35,35,117,35,114,35,35,35,35,-30,]),'}':([9,11,14,16,18,19,22,23,24,35,47,48,49,50,67,74,75,76,77,79,85,86,87,88,89,90,91,94,95,100,102,108,109,115,120,122,127,132,134,],[-54,17,-8,-54,-54,-54,30,-6,-7,-50,-49,-51,-52,-53,94,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-17,-48,-33,-16,-22,125,-20,-27,-32,-19,-31,]),':':([15,26,33,71,114,],[20,32,52,98,124,]),'(':([15,31,35,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,84,92,93,95,96,101,103,105,117,119,121,126,133,],[21,42,55,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,105,42,42,42,42,42,42,42,126,42,42,42,42,]),')':([21,27,28,29,34,35,47,48,49,50,51,53,55,73,74,75,76,77,79,80,81,82,85,86,87,88,89,90,91,94,100,102,103,105,109,116,118,120,122,126,127,131,132,134,],[-54,33,-13,-14,-54,-50,-49,-51,-52,-53,-15,-12,-54,100,-37,-38,-39,-40,-18,102,-35,-36,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-54,-54,-22,-34,127,-20,-27,-54,-32,134,-19,-31,]),'ASSIGN':([25,35,111,],[31,54,121,]),',':([28,35,47,48,49,50,51,70,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,109,111,120,122,127,129,132,134,],[34,-50,-49,-51,-52,-53,-15,97,-37,-38,-39,-40,-18,103,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-26,-20,-27,-32,-25,-19,-31,]),'IF':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'WHILE':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'LET':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'CASE':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'NEW':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'ISVOID':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'NOT':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'~':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'STRING':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'TRUE':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'FALSE':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'INT':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'@':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,56,-49,-51,-52,-53,56,56,56,56,56,-37,56,56,56,56,56,56,56,56,56,56,56,56,-21,-48,-33,56,56,56,56,-20,-27,-32,56,56,-19,-31,56,]),'.':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,83,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,57,-49,-51,-52,-53,57,57,57,57,57,-37,57,57,57,57,57,104,57,57,57,57,57,57,57,-21,-48,-33,57,57,57,57,-20,-27,-32,57,57,-19,-31,57,]),'+':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,58,-49,-51,-52,-53,58,58,58,58,58,-37,-38,58,-40,58,58,-41,-42,-43,-44,58,58,58,-21,-48,-33,58,58,58,58,-20,-27,-32,58,58,-19,-31,58,]),'-':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,59,-49,-51,-52,-53,59,59,59,59,59,-37,-38,59,-40,59,59,-41,-42,-43,-44,59,59,59,-21,-48,-33,59,59,59,59,-20,-27,-32,59,59,-19,-31,59,]),'/':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,60,-49,-51,-52,-53,60,60,60,60,60,-37,-38,60,-40,60,60,60,60,-43,-44,60,60,60,-21,-48,-33,60,60,60,60,-20,-27,-32,60,60,-19,-31,60,]),'*':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,61,-49,-51,-52,-53,61,61,61,61,61,-37,-38,61,-40,61,61,61,61,-43,-44,61,61,61,-21,-48,-33,61,61,61,61,-20,-27,-32,61,61,-19,-31,61,]),'<':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,62,-49,-51,-52,-53,62,62,62,62,62,-37,-38,62,-40,62,62,-41,-42,-43,-44,None,None,None,-21,-48,-33,62,62,62,62,-20,-27,-32,62,62,-19,-31,62,]),'LESSEQ':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,63,-49,-51,-52,-53,63,63,63,63,63,-37,-38,63,-40,63,63,-41,-42,-43,-44,None,None,None,-21,-48,-33,63,63,63,63,-20,-27,-32,63,63,-19,-31,63,]),'=':([35,36,47,48,49,50,65,66,68,72,73,74,75,76,77,79,81,85,86,87,88,89,90,91,94,100,102,106,107,109,115,120,122,127,128,129,132,134,135,],[-50,64,-49,-51,-52,-53,64,64,64,64,64,-37,-38,64,-40,64,64,-41,-42,-43,-44,None,None,None,-21,-48,-33,64,64,64,64,-20,-27,-32,64,64,-19,-31,64,]),'THEN':([35,47,48,49,50,65,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,109,120,122,127,132,134,],[-50,-49,-51,-52,-53,92,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-20,-27,-32,-19,-31,]),'LOOP':([35,47,48,49,50,66,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,109,120,122,127,132,134,],[-50,-49,-51,-52,-53,93,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-20,-27,-32,-19,-31,]),'OF':([35,47,48,49,50,72,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,109,120,122,127,132,134,],[-50,-49,-51,-52,-53,99,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-20,-27,-32,-19,-31,]),'ELSE':([35,47,48,49,50,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,106,109,120,122,127,132,134,],[-50,-49,-51,-52,-53,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,119,-22,-20,-27,-32,-19,-31,]),'POOL':([35,47,48,49,50,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,107,109,120,122,127,132,134,],[-50,-49,-51,-52,-53,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,120,-22,-20,-27,-32,-19,-31,]),'FI':([35,47,48,49,50,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,109,120,122,127,128,132,134,],[-50,-49,-51,-52,-53,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-20,-27,-32,132,-19,-31,]),'IN':([35,47,48,49,50,69,70,74,75,76,77,79,85,86,87,88,89,90,91,94,100,102,109,110,111,120,122,127,129,132,134,],[-50,-49,-51,-52,-53,96,-24,-37,-38,-39,-40,-18,-41,-42,-43,-44,-45,-46,-47,-21,-48,-33,-22,-23,-26,-20,-27,-32,-25,-19,-31,]),'ESAC':([112,113,123,136,],[122,-29,-28,-30,]),'RET':([130,],[133,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,5,],[2,7,]),'class':([0,5,],[3,3,]),'feature_list':([9,16,18,19,],[11,22,23,24,]),'attribute':([9,16,18,19,],[12,12,12,12,]),'method':([9,16,18,19,],[13,13,13,13,]),'empty':([9,16,18,19,21,34,55,103,105,126,],[14,14,14,14,29,29,82,82,82,82,]),'params_list':([21,34,],[27,53,]),'param':([21,34,],[28,28,]),'expression':([31,37,38,39,41,42,44,45,46,54,55,58,59,60,61,62,63,64,92,93,95,96,101,103,105,119,121,126,133,],[36,65,66,68,72,73,75,76,77,79,81,85,86,87,88,89,90,91,106,107,68,109,115,81,81,128,129,81,135,]),'expression_list':([39,95,],[67,108,]),'let_list':([40,97,],[69,110,]),'let_single':([40,97,],[70,70,]),'args_list':([55,103,105,126,],[80,116,118,131,]),'case_list':([99,113,],[112,123,]),'case_single':([99,113,],[113,113,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','parsing_rules.py',35),
  ('class_list -> class ; class_list','class_list',3,'p_class_list','parsing_rules.py',40),
  ('class_list -> class ;','class_list',2,'p_class_list','parsing_rules.py',41),
  ('class -> CLASS TYPE INHERITS TYPE { feature_list }','class',7,'p_class','parsing_rules.py',49),
  ('class -> CLASS TYPE { feature_list }','class',5,'p_class','parsing_rules.py',50),
  ('feature_list -> attribute ; feature_list','feature_list',3,'p_feature_list','parsing_rules.py',60),
  ('feature_list -> method ; feature_list','feature_list',3,'p_feature_list','parsing_rules.py',61),
  ('feature_list -> empty','feature_list',1,'p_feature_list','parsing_rules.py',62),
  ('attribute -> ID : TYPE ASSIGN expression','attribute',5,'p_attribute','parsing_rules.py',70),
  ('attribute -> ID : TYPE','attribute',3,'p_attribute','parsing_rules.py',71),
  ('method -> ID ( params_list ) : TYPE { expression }','method',9,'p_method','parsing_rules.py',81),
  ('params_list -> param , params_list','params_list',3,'p_params_list','parsing_rules.py',87),
  ('params_list -> param','params_list',1,'p_params_list','parsing_rules.py',88),
  ('params_list -> empty','params_list',1,'p_params_list_empty','parsing_rules.py',96),
  ('param -> ID : TYPE','param',3,'p_param','parsing_rules.py',101),
  ('expression_list -> expression ; expression_list','expression_list',3,'p_expression_list','parsing_rules.py',107),
  ('expression_list -> expression ;','expression_list',2,'p_expression_list','parsing_rules.py',108),
  ('expression -> ID ASSIGN expression','expression',3,'p_expression_assigment','parsing_rules.py',116),
  ('expression -> IF expression THEN expression ELSE expression FI','expression',7,'p_expression_if_then_else','parsing_rules.py',122),
  ('expression -> WHILE expression LOOP expression POOL','expression',5,'p_expression_while','parsing_rules.py',128),
  ('expression -> { expression_list }','expression',3,'p_expression_block','parsing_rules.py',134),
  ('expression -> LET let_list IN expression','expression',4,'p_expression_let_in','parsing_rules.py',140),
  ('let_list -> let_single , let_list','let_list',3,'p_let_list','parsing_rules.py',146),
  ('let_list -> let_single','let_list',1,'p_let_list','parsing_rules.py',147),
  ('let_single -> ID : TYPE ASSIGN expression','let_single',5,'p_let_single','parsing_rules.py',155),
  ('let_single -> ID : TYPE','let_single',3,'p_let_single','parsing_rules.py',156),
  ('expression -> CASE expression OF case_list ESAC','expression',5,'p_expression_case','parsing_rules.py',165),
  ('case_list -> case_single case_list','case_list',2,'p_case_list','parsing_rules.py',171),
  ('case_list -> case_single','case_list',1,'p_case_list','parsing_rules.py',172),
  ('case_single -> ID : TYPE RET expression ;','case_single',6,'p_case_single','parsing_rules.py',180),
  ('expression -> expression @ TYPE . ID ( args_list )','expression',8,'p_expression_dispatch','parsing_rules.py',186),
  ('expression -> expression . ID ( args_list )','expression',6,'p_expression_dispatch','parsing_rules.py',187),
  ('expression -> ID ( args_list )','expression',4,'p_expression_dispatch','parsing_rules.py',188),
  ('args_list -> expression , args_list','args_list',3,'p_args_list','parsing_rules.py',203),
  ('args_list -> expression','args_list',1,'p_args_list','parsing_rules.py',204),
  ('args_list -> empty','args_list',1,'p_args_list_empty','parsing_rules.py',212),
  ('expression -> NEW TYPE','expression',2,'p_expression_instatiate','parsing_rules.py',217),
  ('expression -> ISVOID expression','expression',2,'p_expression_isvoid','parsing_rules.py',223),
  ('expression -> NOT expression','expression',2,'p_expression_not','parsing_rules.py',229),
  ('expression -> ~ expression','expression',2,'p_expression_complement','parsing_rules.py',235),
  ('expression -> expression + expression','expression',3,'p_expression_plus','parsing_rules.py',241),
  ('expression -> expression - expression','expression',3,'p_expression_minus','parsing_rules.py',247),
  ('expression -> expression / expression','expression',3,'p_expression_div','parsing_rules.py',253),
  ('expression -> expression * expression','expression',3,'p_expression_star','parsing_rules.py',259),
  ('expression -> expression < expression','expression',3,'p_expression_less','parsing_rules.py',265),
  ('expression -> expression LESSEQ expression','expression',3,'p_expression_lesseq','parsing_rules.py',271),
  ('expression -> expression = expression','expression',3,'p_expression_equals','parsing_rules.py',277),
  ('expression -> ( expression )','expression',3,'p_expression_parentheses','parsing_rules.py',283),
  ('expression -> STRING','expression',1,'p_expression_string','parsing_rules.py',289),
  ('expression -> ID','expression',1,'p_expression_variable','parsing_rules.py',295),
  ('expression -> TRUE','expression',1,'p_expression_true','parsing_rules.py',301),
  ('expression -> FALSE','expression',1,'p_expression_false','parsing_rules.py',307),
  ('expression -> INT','expression',1,'p_expression_int','parsing_rules.py',313),
  ('empty -> <empty>','empty',0,'p_empty','parsing_rules.py',319),
]
