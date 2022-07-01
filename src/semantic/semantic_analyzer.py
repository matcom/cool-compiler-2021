from .visitor import *

class MySemanticAnalyzer:
	def __init__(self, ast):
		self.ast = ast
		self.errors = []

	def analyze(self):

		type_collector = TypeCollector(self.errors)
		type_collector.visit(self.ast)
		context = type_collector.context

		#building types
		type_builder = TypeBuilder(context, self.errors)
		type_builder.visit(self.ast)

		if len(self.errors) > 0: 
			return context, None

		#checking types
		type_checker = TypeChecker(context, self.errors)
		scope = type_checker.visit(self.ast)

		return context, scope