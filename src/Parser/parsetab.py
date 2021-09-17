
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightLDASHINleftNOTleftLEQUALLESSEQUALleftPLUSMINUSleftSTARDIVIDEleftISVOIDleftTILDEleftATleftDOTAT BOOL CASE CLASS COLON COMMA DIVIDE DOT ELSE EQUAL ESAC FI GEQUAL ID IF IN INHERITS INT ISVOID LCURLY LDASH LEQUAL LESS LET LOOP LPAREN MINUS NEW NOT OF PLUS POOL RCURLY RPAREN SEMICOLON STAR STRING THEN TILDE TYPE WHILEprogram : classlistclasslist : defclass SEMICOLON\n                     | defclass SEMICOLON classlistdefclass : CLASS TYPE LCURLY featurelist RCURLY\n                    | CLASS TYPE INHERITS TYPE LCURLY featurelist RCURLYfeaturelist : defmethods SEMICOLON featurelist\n                       | defattributes SEMICOLON featurelist\n                       | defattributes : ID COLON TYPE \n                         | ID COLON TYPE LDASH expressiondefmethods : ID LPAREN parameterslist RPAREN COLON TYPE LCURLY expression RCURLYparameterslist : parameters\n                          | parameters : ID COLON TYPE\n                      | ID COLON TYPE COMMA parameters expression : ID LDASH expressionexpression : ID LPAREN argumentslist RPAREN\n                      | expression DOT ID LPAREN argumentslist RPAREN\n                      | expression AT TYPE DOT ID LPAREN argumentslist RPARENargumentslist : argument\n                         | argument : expression\n                    | expression COMMA argumentexpression : IF expression THEN expression ELSE expression FIexpression : WHILE expression LOOP expression POOLexpression : LCURLY expressionlist RCURLYexpressionlist : expression SEMICOLON\n                          | expression SEMICOLON expressionlistexpression : LET variableslist IN expressionvariableslist : variable\n                         | variable COMMA variableslistvariable : ID COLON TYPE\n                    | ID COLON TYPE LDASH expressionexpression : CASE expression OF typetestlist ESACtypetestlist : ID COLON TYPE GEQUAL expression SEMICOLON\n                        | ID COLON TYPE GEQUAL expression SEMICOLON typetestlistexpression : NEW TYPEexpression : ISVOID expressionexpression : expression PLUS expressionexpression : expression MINUS expressionexpression : expression STAR expressionexpression : expression DIVIDE expressionexpression : expression LESS expressionexpression : expression LEQUAL expressionexpression : expression EQUAL expressionexpression : TILDE expressionexpression : NOT expressionexpression : LPAREN expression RPARENexpression : IDexpression : INTexpression : STRINGexpression : BOOL'
    
_lr_action_items = {'CLASS':([0,5,],[4,4,]),'$end':([1,2,5,7,],[0,-1,-2,-3,]),'SEMICOLON':([3,11,12,15,26,31,34,35,46,47,48,66,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,107,112,117,119,121,127,129,130,],[5,16,17,-4,-9,-5,-49,-10,-50,-51,-52,94,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-11,-25,-34,-18,-24,-19,131,]),'TYPE':([4,9,19,28,33,42,54,97,120,],[6,14,26,32,50,71,82,109,125,]),'LCURLY':([6,14,30,36,37,38,39,41,43,44,45,50,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[8,20,39,39,39,39,39,39,39,39,39,76,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'INHERITS':([6,],[9,]),'RCURLY':([8,10,16,17,20,21,22,27,34,46,47,48,65,71,72,73,74,77,83,84,85,86,87,88,89,90,93,94,99,100,106,107,117,119,121,127,129,],[-8,15,-8,-8,-8,-6,-7,31,-49,-50,-51,-52,93,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-27,112,-17,-28,-29,-25,-34,-18,-24,-19,]),'ID':([8,16,17,18,20,30,36,37,38,39,40,41,43,44,45,49,51,52,53,55,56,57,58,59,60,61,76,91,92,94,95,96,98,101,102,103,116,118,122,128,131,],[13,13,13,23,13,34,34,34,34,34,69,34,34,34,34,23,34,34,81,34,34,34,34,34,34,34,34,34,34,34,34,69,111,34,34,115,34,34,34,34,111,]),'LPAREN':([13,30,34,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,81,91,92,94,95,101,102,115,116,118,122,128,],[18,36,52,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,102,36,36,36,36,36,36,122,36,36,36,36,]),'COLON':([13,23,29,69,111,],[19,28,33,97,120,]),'RPAREN':([18,24,25,32,34,46,47,48,52,62,71,72,73,74,75,77,78,79,80,83,84,85,86,87,88,89,90,93,100,102,107,113,114,117,119,121,122,126,127,129,],[-13,29,-12,-14,-49,-50,-51,-52,-21,90,-37,-38,-46,-47,-15,-16,100,-20,-22,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-21,-29,-23,121,-25,-34,-18,-21,129,-24,-19,]),'LDASH':([26,34,109,],[30,51,118,]),'IF':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'WHILE':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'LET':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'CASE':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'NEW':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'ISVOID':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'TILDE':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'NOT':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'INT':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'STRING':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'BOOL':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'COMMA':([32,34,46,47,48,68,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,100,107,109,117,119,121,124,127,129,],[49,-49,-50,-51,-52,96,-37,-38,-46,-47,-16,101,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-32,-25,-34,-18,-33,-24,-19,]),'DOT':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,82,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,53,-50,-51,-52,53,53,53,53,53,-37,53,53,53,53,53,103,53,53,53,53,53,53,53,-48,-26,53,-17,53,53,53,-25,-34,-18,53,53,-24,-19,53,]),'AT':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,54,-50,-51,-52,54,54,54,54,54,-37,54,54,54,54,54,54,54,54,54,54,54,54,-48,-26,54,-17,54,54,54,-25,-34,-18,54,54,-24,-19,54,]),'PLUS':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,55,-50,-51,-52,55,55,55,55,55,-37,-38,-46,55,55,55,-39,-40,-41,-42,55,55,55,-48,-26,55,-17,55,55,55,-25,-34,-18,55,55,-24,-19,55,]),'MINUS':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,56,-50,-51,-52,56,56,56,56,56,-37,-38,-46,56,56,56,-39,-40,-41,-42,56,56,56,-48,-26,56,-17,56,56,56,-25,-34,-18,56,56,-24,-19,56,]),'STAR':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,57,-50,-51,-52,57,57,57,57,57,-37,-38,-46,57,57,57,57,57,-41,-42,57,57,57,-48,-26,57,-17,57,57,57,-25,-34,-18,57,57,-24,-19,57,]),'DIVIDE':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,58,-50,-51,-52,58,58,58,58,58,-37,-38,-46,58,58,58,58,58,-41,-42,58,58,58,-48,-26,58,-17,58,58,58,-25,-34,-18,58,58,-24,-19,58,]),'LESS':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,59,-50,-51,-52,59,59,59,59,59,-37,-38,-46,59,59,59,-39,-40,-41,-42,-43,-44,-45,-48,-26,59,-17,59,59,59,-25,-34,-18,59,59,-24,-19,59,]),'LEQUAL':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,60,-50,-51,-52,60,60,60,60,60,-37,-38,-46,60,60,60,-39,-40,-41,-42,-43,-44,-45,-48,-26,60,-17,60,60,60,-25,-34,-18,60,60,-24,-19,60,]),'EQUAL':([34,35,46,47,48,62,63,64,66,70,71,72,73,74,77,80,83,84,85,86,87,88,89,90,93,99,100,104,105,107,117,119,121,123,124,127,129,130,],[-49,61,-50,-51,-52,61,61,61,61,61,-37,-38,-46,61,61,61,-39,-40,-41,-42,-43,-44,-45,-48,-26,61,-17,61,61,61,-25,-34,-18,61,61,-24,-19,61,]),'THEN':([34,46,47,48,63,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,107,117,119,121,127,129,],[-49,-50,-51,-52,91,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-25,-34,-18,-24,-19,]),'LOOP':([34,46,47,48,64,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,107,117,119,121,127,129,],[-49,-50,-51,-52,92,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-25,-34,-18,-24,-19,]),'OF':([34,46,47,48,70,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,107,117,119,121,127,129,],[-49,-50,-51,-52,98,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-25,-34,-18,-24,-19,]),'ELSE':([34,46,47,48,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,104,107,117,119,121,127,129,],[-49,-50,-51,-52,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,116,-29,-25,-34,-18,-24,-19,]),'POOL':([34,46,47,48,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,105,107,117,119,121,127,129,],[-49,-50,-51,-52,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,117,-29,-25,-34,-18,-24,-19,]),'FI':([34,46,47,48,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,107,117,119,121,123,127,129,],[-49,-50,-51,-52,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-25,-34,-18,127,-24,-19,]),'IN':([34,46,47,48,67,68,71,72,73,74,77,83,84,85,86,87,88,89,90,93,100,107,108,109,117,119,121,124,127,129,],[-49,-50,-51,-52,95,-30,-37,-38,-46,-47,-16,-39,-40,-41,-42,-43,-44,-45,-48,-26,-17,-29,-31,-32,-25,-34,-18,-33,-24,-19,]),'ESAC':([110,131,132,],[119,-35,-36,]),'GEQUAL':([125,],[128,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'classlist':([0,5,],[2,7,]),'defclass':([0,5,],[3,3,]),'featurelist':([8,16,17,20,],[10,21,22,27,]),'defmethods':([8,16,17,20,],[11,11,11,11,]),'defattributes':([8,16,17,20,],[12,12,12,12,]),'parameterslist':([18,],[24,]),'parameters':([18,49,],[25,75,]),'expression':([30,36,37,38,39,41,43,44,45,51,52,55,56,57,58,59,60,61,76,91,92,94,95,101,102,116,118,122,128,],[35,62,63,64,66,70,72,73,74,77,80,83,84,85,86,87,88,89,99,104,105,66,107,80,80,123,124,80,130,]),'expressionlist':([39,94,],[65,106,]),'variableslist':([40,96,],[67,108,]),'variable':([40,96,],[68,68,]),'argumentslist':([52,102,122,],[78,114,126,]),'argument':([52,101,102,122,],[79,113,79,79,]),'typetestlist':([98,131,],[110,132,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> classlist','program',1,'p_programm','parser.py',34),
  ('classlist -> defclass SEMICOLON','classlist',2,'p_classlist','parser.py',38),
  ('classlist -> defclass SEMICOLON classlist','classlist',3,'p_classlist','parser.py',39),
  ('defclass -> CLASS TYPE LCURLY featurelist RCURLY','defclass',5,'p_defclass','parser.py',46),
  ('defclass -> CLASS TYPE INHERITS TYPE LCURLY featurelist RCURLY','defclass',7,'p_defclass','parser.py',47),
  ('featurelist -> defmethods SEMICOLON featurelist','featurelist',3,'p_featurelist','parser.py',54),
  ('featurelist -> defattributes SEMICOLON featurelist','featurelist',3,'p_featurelist','parser.py',55),
  ('featurelist -> <empty>','featurelist',0,'p_featurelist','parser.py',56),
  ('defattributes -> ID COLON TYPE','defattributes',3,'p_defattributes','parser.py',63),
  ('defattributes -> ID COLON TYPE LDASH expression','defattributes',5,'p_defattributes','parser.py',64),
  ('defmethods -> ID LPAREN parameterslist RPAREN COLON TYPE LCURLY expression RCURLY','defmethods',9,'p_defmethods','parser.py',71),
  ('parameterslist -> parameters','parameterslist',1,'p_parameterslist','parser.py',75),
  ('parameterslist -> <empty>','parameterslist',0,'p_parameterslist','parser.py',76),
  ('parameters -> ID COLON TYPE','parameters',3,'p_parameters','parser.py',83),
  ('parameters -> ID COLON TYPE COMMA parameters','parameters',5,'p_parameters','parser.py',84),
  ('expression -> ID LDASH expression','expression',3,'p_expression_assignment','parser.py',91),
  ('expression -> ID LPAREN argumentslist RPAREN','expression',4,'p_expression_dispatch','parser.py',95),
  ('expression -> expression DOT ID LPAREN argumentslist RPAREN','expression',6,'p_expression_dispatch','parser.py',96),
  ('expression -> expression AT TYPE DOT ID LPAREN argumentslist RPAREN','expression',8,'p_expression_dispatch','parser.py',97),
  ('argumentslist -> argument','argumentslist',1,'p_argumentslist','parser.py',107),
  ('argumentslist -> <empty>','argumentslist',0,'p_argumentslist','parser.py',108),
  ('argument -> expression','argument',1,'p_argument','parser.py',115),
  ('argument -> expression COMMA argument','argument',3,'p_argument','parser.py',116),
  ('expression -> IF expression THEN expression ELSE expression FI','expression',7,'p_expression_conditionals','parser.py',123),
  ('expression -> WHILE expression LOOP expression POOL','expression',5,'p_expression_loops','parser.py',127),
  ('expression -> LCURLY expressionlist RCURLY','expression',3,'p_expression_blocks','parser.py',131),
  ('expressionlist -> expression SEMICOLON','expressionlist',2,'p_expressionlist','parser.py',135),
  ('expressionlist -> expression SEMICOLON expressionlist','expressionlist',3,'p_expressionlist','parser.py',136),
  ('expression -> LET variableslist IN expression','expression',4,'p_expression_let','parser.py',143),
  ('variableslist -> variable','variableslist',1,'p_variableslist','parser.py',147),
  ('variableslist -> variable COMMA variableslist','variableslist',3,'p_variableslist','parser.py',148),
  ('variable -> ID COLON TYPE','variable',3,'p_variable','parser.py',155),
  ('variable -> ID COLON TYPE LDASH expression','variable',5,'p_variable','parser.py',156),
  ('expression -> CASE expression OF typetestlist ESAC','expression',5,'p_expression_case','parser.py',163),
  ('typetestlist -> ID COLON TYPE GEQUAL expression SEMICOLON','typetestlist',6,'p_typetestlist','parser.py',167),
  ('typetestlist -> ID COLON TYPE GEQUAL expression SEMICOLON typetestlist','typetestlist',7,'p_typetestlist','parser.py',168),
  ('expression -> NEW TYPE','expression',2,'p_expression_new','parser.py',175),
  ('expression -> ISVOID expression','expression',2,'p_expression_isvoid','parser.py',179),
  ('expression -> expression PLUS expression','expression',3,'p_expression_plus','parser.py',183),
  ('expression -> expression MINUS expression','expression',3,'p_expression_minus','parser.py',187),
  ('expression -> expression STAR expression','expression',3,'p_expression_star','parser.py',191),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_divide','parser.py',195),
  ('expression -> expression LESS expression','expression',3,'p_expression_less','parser.py',199),
  ('expression -> expression LEQUAL expression','expression',3,'p_expression_lequal','parser.py',203),
  ('expression -> expression EQUAL expression','expression',3,'p_expression_equal','parser.py',207),
  ('expression -> TILDE expression','expression',2,'p_expression_complement','parser.py',211),
  ('expression -> NOT expression','expression',2,'p_expression_not','parser.py',215),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_paren','parser.py',219),
  ('expression -> ID','expression',1,'p_expression_atomic_id','parser.py',223),
  ('expression -> INT','expression',1,'p_expression_atomic_int','parser.py',227),
  ('expression -> STRING','expression',1,'p_expression_atomic_string','parser.py',231),
  ('expression -> BOOL','expression',1,'p_expression_atomic_bool','parser.py',235),
]
