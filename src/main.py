import sys
from errors import CompilerError
from my_lexer import MyLexer
from my_parser import MyParser
from semantics import SemanticsAndTypes
from code_to_cil import CodeToCIL
from code_gen import CodeGen

def main():

	input_file = sys.argv[1]
		
	if not str(input_file).endswith(".cl"):
			print(CompilerError(0, 0, "Cool program files must end with a .cl extension."))
			exit(1)
	
	input = ""
	try:
		with open(input_file, encoding="utf-8") as file:
			input += file.read()
	except (IOError, FileNotFoundError):
		print(CompilerError(0, 0, "Error! File \"{}\" was not found".format(input_file)))
		exit(1)
	
	#Lexical and Syntax Analysis
	lexer = MyLexer(input)
	lexer.build()
	if lexer.check():
		exit(1)
	parser = MyParser(lexer)
	parser.build()
	ast = parser.parse(input)
	if parser.errors:
		exit(1)
	
	#Semantic and Types Analysis
	st = SemanticsAndTypes(ast)
	if not st.check():
		exit(1)
	
	#Code Generation
	ctcil = CodeToCIL(st.types)
	cil = ctcil.visit(ast)
	cg = CodeGen()
	cg.visit(cil, st.types)
	
	with open(input_file[0:-3] + ".mips", 'w') as file:
		file.writelines(cg.output)
		file.close()
	
if __name__ == '__main__':
	main()