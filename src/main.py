import sys
from errors import CompilerError
from my_lexer import MyLexer
from my_parser import MyParser
from semantics import SemanticsAndTypes
from code_to_cil import CodeToCIL
from code_gen import CodeGen

def main():
	files = sys.argv[1:]
	if len(files) == 0:
		print(CompilerError(0, 0, "No file is given to coolc compiler."))
		return

	# Check all files have the *.cl extension.
	for file in files:
		if not str(file).endswith(".cl"):
			print(CompilerError(0, 0, "Cool program files must end with a .cl extension."))
			return
	
	input = ""
	
	# Read all files source codes and store it in memory.
	for file in files:
		try:
			with open(file, encoding="utf-8") as file:
				input += file.read()
		except (IOError, FileNotFoundError):
			print(CompilerError(0, 0, "Error! File \"{0}\" was not found".format(file)))
			return
	
	#Lexical and Syntax Analysis
	lexer = MyLexer(input)
	lexer.build()
	if lexer.check():
		exit()
	parser = MyParser(lexer)
	parser.build()
	ast = parser.parse(input)
	if parser.errors:
		exit()
	
	#Semantic and Types Analysis
	st = SemanticsAndTypes(ast)
	if not st.check():
		exit()
	
	#Code Generation
	ctcil = CodeToCIL(st.types)
	cil = ctcil.visit(ast)
	cg = CodeGen()
	cg.visit(cil, st.types)
	
	f = open(files[0][:-3] + ".mips", 'w')
	f.writelines(cg.output)
	f.close()
	
if __name__ == '__main__':
	main()