import ply.yacc as yacc
import cool_ast as ast
from my_lexer import tokens
from errors import SyntacticError

class MyParser:
	def __init__(self, lexer):
		self.tokens = tokens
		self.lexer = lexer
		self.parser = None
		self.errors = False
	
	#Build the parser
	def build(self, **kwargs):
		self.lexer.build()
		self.parser = yacc.yacc(module=self, **kwargs)
	
	def parse(self, code):
		try:			
			return self.parser.parse(code)
		except:
			return None
	
	#Precedence rules
	precedence = (
		('right', 'ASSIGN'),
		('left', 'NOT'),
		('nonassoc', 'LT', 'LTEQ', 'EQ'),
		('left', 'PLUS', 'MINUS'),
		('left', 'MULTIPLY', 'DIVIDE'),
		('right', 'ISVOID'),
		('right', 'COMPLEMENT'),
		('left', 'AT'),
		('left', 'DOT')
	)

	def p_program(self, parse):
		'''program : class_expresion SEMICOLON class_list'''
		parse[0] = ast.ProgramNode([parse[1]] + parse[3])
	
	def p_class_list(self, parse):
		'''class_list : class_expresion SEMICOLON class_list
					 | empty'''
		if len(parse) > 2:
			parse[0] = [parse[1]] + parse[3]
		else:
			parse[0] = []
		
	def p_class_expresion(self, parse):
		'''class_expresion : CLASS TYPE LBRACE feature_list
						   | CLASS TYPE INHERITS TYPE LBRACE feature_list'''
		if parse[3] == '{':
			parse[0] = ast.ClassNode(parse[2], None, parse[4], parse.lineno(2), parse.lexpos(2))
		elif parse[3] == 'inherits':
			parse[0] = ast.ClassNode(parse[2], parse[4], parse[6], parse.lineno(2), parse.lexpos(2), parse.lexpos(4))
		
	def p_feature_list(self, parse):
		'''feature_list : method_decl feature_list
						| property_decl feature_list
						| RBRACE'''
		if len(parse) > 2:
			parse[0] = [parse[1]] + parse[2]
		else:
			parse[0] = []
			
	def p_property_decl(self, parse):
		'''property_decl : declare_expresion SEMICOLON'''
		parse[0] = ast.PropertyNode(parse[1], parse[1].line, parse[1].index)	
		
	def p_declare_expresion(self, parse):
		'''declare_expresion : ID COLON TYPE ASSIGN expr
							 | ID COLON TYPE'''
		if len(parse) > 4:
			parse[0] = ast.DeclarationNode(parse[1], parse[3], parse[5], parse.lineno(1), parse.lexpos(1), parse.lexpos(3),0)
		else:
			parse[0] = ast.DeclarationNode(parse[1], parse[3], None, parse.lineno(1), parse.lexpos(1), parse.lexpos(3),0)
	
	def p_method_decl(self, parse):
		'''method_decl : ID LPAREN formal RPAREN COLON TYPE LBRACE expr RBRACE SEMICOLON'''
		parse[0] = ast.MethodNode(parse[1], parse[3], parse[6], parse[8], parse.lineno(1), parse.lexpos(1), parse.lexpos(6))
		
	def p_formal(self, parse):
		''' formal : declare_method formal_a
				   | empty '''
		if len(parse) > 2:
			parse[0] = [parse[1]] + parse[2]
		else:
			parse[0] = []

	def p_formal_a(self, parse):
		'''formal_a : COMMA declare_method formal_a
					| empty'''
		if len(parse) > 2:
			parse[0] = [parse[2]] + parse[3]
		else:
			parse[0] = []
		
	def p_declare_method(self, parse):
		'''declare_method : ID COLON TYPE'''
		parse[0] = ast.DeclarationNode(parse[1], parse[3], None, parse.lineno(1), parse.lexpos(1), parse.lexpos(3), 0)
		
	def p_expr(self, parse):
		'''expr : assign_expresion
				| while_expresion
				| v_expr'''
		parse[0] = parse[1]
		
	def p_assign_expresion(self, parse):
		'''assign_expresion : ID ASSIGN expr'''
		parse[0] = ast.AssignNode(parse[1], parse[3], parse.lineno(1), parse.lexpos(1), parse.lexpos(2))
		
	def p_while_expresion(self, parse):
		'''while_expresion : WHILE v_expr LOOP expr POOL'''
		parse[0] = ast.WhileNode(parse[2], parse[4], parse.lineno(1), parse.lexpos(1), parse[2].index)
		
	def p_v_expr(self, parse):
		'''v_expr : conditional_expresion
				  | let_expresion
				  | case_expresion
				  | dispatch_expresion
				  | dispatch_instance
				  | block_expresion
				  | binary_operator
				  | neg
				  | compl
				  | is_void
				  | new_expresion
				  | term
				  | comparison_expresion'''
		parse[0] = parse[1]
		
	def p_conditional_expresion(self, parse):
		'''conditional_expresion : IF v_expr THEN expr ELSE expr FI'''
		parse[0] = ast.IfNode(parse[2], parse[4], parse[6], parse.lineno(1), parse.lexpos(1))
		
	def p_let_expresion(self, parse):
		'''let_expresion : LET let_declr_list IN expr'''
		parse[0] = ast.LetInNode(parse[2], parse[4], parse.lineno(1), parse.lexpos(1))
		
	def p_let_declr_list(self, parse):
		'''let_declr_list : declare_expresion let_declr_list_a'''
		parse[0] = [parse[1]] + parse[2]

	def p_let_declr_list_a(self, parse):
		'''let_declr_list_a : COMMA declare_expresion let_declr_list_a
							| empty'''
		if len(parse) > 3:
			parse[0] = [parse[2]] + parse[3]
		else:
			parse[0] = []
		
	def p_case_expresion(self, parse):
		'''case_expresion : CASE expr OF case_list ESAC'''
		parse[0] = ast.CaseNode(parse[2], parse[4], parse.lineno(1), parse.lexpos(1))
		
	def p_case_list(self, parse):
		'''case_list : declare_method ACTION expr SEMICOLON case_list_a'''
		parse[0] = [ast.CaseItemNode(parse[1], parse[3], parse[1].line, parse[1].index2)] + parse[5]
		
	def p_case_list_a(self, parse):
		'''case_list_a : declare_method ACTION expr SEMICOLON case_list_a
					   | empty'''
		if len(parse) > 2:
			parse[0] = [ast.CaseItemNode(parse[1], parse[3], parse[1].line, parse[1].index2)] + parse[5]
		else:
			parse[0] = []
			
	def p_dispatch_expresion(self, parse):
		'''dispatch_expresion : ID LPAREN dispatch_p_list RPAREN '''
		parse[0] = ast.DispatchNode(parse[1], parse[3], parse.lineno(1), parse.lexpos(1))
		
	def p_dispatch_p_list(self, parse):
		'''dispatch_p_list : v_expr dispatch_p_list_a
						   | empty'''
		if len(parse) > 2:
			parse[0] =  [parse[1]] + parse[2]
		else:
			parse[0] = []

	def p_dispatch_p_list_a(self, parse):
		'''dispatch_p_list_a : COMMA v_expr dispatch_p_list_a
							 | empty'''
		if len(parse) > 2:
			parse[0] =  [parse[2]] + parse[3]
		else:
			parse[0] = []
			
	def p_dispatch_instance(self, parse):
		'''dispatch_instance : v_expr DOT ID LPAREN dispatch_p_list RPAREN
							 | v_expr AT TYPE DOT ID LPAREN dispatch_p_list RPAREN '''
		if len(parse) > 7:
			parse[0] = ast.DispatchParentInstanceNode(parse[1], parse[3], parse[5], parse[7], parse.lineno(2), parse[1].index, parse.lexpos(5), parse.lexpos(3))
		else:
			parse[0] = ast.DispatchInstanceNode(parse[1], parse[3], parse[5], parse.lineno(2), parse[1].index, parse.lexpos(3))

	def p_block_expresion(self, parse):
		'''block_expresion : LBRACE block_expr RBRACE'''
		parse[0] = ast.BlockNode(parse[2], parse.lineno(1), parse.lexpos(1))
		
	def p_block_expr(self, parse):
		'''block_expr : expr SEMICOLON block_expr_a'''
		parse[0] = [parse[1]] + parse[3]

	def p_block_expr_a(self, parse):
		'''block_expr_a : expr SEMICOLON block_expr_a
						| empty'''
		if len(parse) > 2:
			parse[0] = [parse[1]] + parse[3]
		else:
			parse[0] = []
			
	def p_binary_operator(self, parse):
		'''binary_operator : v_expr PLUS v_expr
						   | v_expr MINUS v_expr
						   | v_expr MULTIPLY v_expr
						   | v_expr DIVIDE v_expr'''
		if parse[2] == '+':
			parse[0] = ast.PlusNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))
		elif parse[2] == '-':
			parse[0] = ast.MinusNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))
		elif parse[2] == '*':
			parse[0] = ast.StarNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))
		elif parse[2] == '/':
			parse[0] = ast.DivNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))

	def p_neg(self, parse):
		'''neg : NOT expr'''
		parse[0] = ast.NotNode(parse[2], parse.lineno(1), parse.lexpos(1), parse.lexpos(1) + 4)

	def p_compl(self, parse):
		'''compl : COMPLEMENT expr'''
		parse[0] = ast.ComplementNode(parse[2], parse.lineno(1), parse.lexpos(1), parse.lexpos(1) + 1)
		
	def p_is_void(self, parse):
		'''is_void : ISVOID expr'''
		parse[0] = ast.IsVoidNode(parse[2], parse.lineno(1), parse.lexpos(1))

	def p_new_expresion(self, parse):
		'''new_expresion : NEW TYPE'''
		parse[0] = ast.NewNode(parse[2], parse.lineno(1), parse.lexpos(1), parse.lexpos(2))
		
	def p_comparison_expresion(self, parse):
		'''comparison_expresion : v_expr LT v_expr
								| v_expr LTEQ v_expr
								| v_expr EQ v_expr'''
		if parse[2] == '<':
			parse[0] = ast.LessThanNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))
		elif parse[2] == '<=':
			parse[0] = ast.LessEqualNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))
		elif parse[2] == '=':
			parse[0] = ast.EqualNode(parse[1], parse[3], parse.lineno(2), parse[1].index, parse.lexpos(2))
			
	def p_term(self, parse):
		'''term : var
				| num
				| str
				| bool
				| negnum
				| LPAREN v_expr RPAREN'''
		if parse[1] == '(':
			parse[0] = parse[2]
		else:
			parse[0] = parse[1]

	def p_var(self, parse):
		'''var : ID'''
		parse[0] = ast.VariableNode(parse[1], parse.lineno(1), parse.lexpos(1))

	def p_num(self, parse):
		'''num : INTEGER'''
		parse[0] = ast.IntegerNode(parse[1], parse.lineno(1), parse.lexpos(1))
		
	def p_str(self, parse):
		'''str : STRING'''
		parse[0] = ast.StringNode(parse[1], parse.lineno(1), parse.lexpos(1))
		
	def p_bool(self, parse):
		'''bool : TRUE
		        | FALSE'''
		parse[0] = ast.BooleanNode(parse[1], parse.lineno(1), parse.lexpos(1))
		
	def p_negnum(self, parse):
		'''negnum : MINUS term'''
		parse[0] = ast.NegationNode(parse[2], parse.lineno(1), parse.lexpos(1))
		
	def p_empty(self, parse):
		'''empty :'''
		pass
	
	#Error rule
	def p_error(self, parse):
		self.errors = True
		if parse:
			print(SyntacticError(parse.lineno, parse.lexpos, "ERROR at or near {}".format(parse.value)))
		else:
			print(SyntacticError(0, 0, "ERROR at or near EOF"))