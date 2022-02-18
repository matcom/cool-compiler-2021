def create_string(name, tag, int_const, value):
	string = f'{name}:\n'
	string += f'		.word	{tag}\n'
	string += f'		.word	6\n'
	string += f'		.word	String_disp\n'
	string += f'		.word	{int_const}\n'
	string += f'		.ascii	"{value}"\n'
	#string += f'		.byte	0\n'
	string += f'		.word	-1\n'
	return string

def create_int(name, tag, value):
	integer = f'{name}:\n'
	integer += f'		.word	{tag}\n'
	integer += f'		.word	4\n'
	integer += f'		.word	Int_disp\n'
	integer += f'		.word	{value}\n'
	integer += f'		.word	-1\n'
	return integer

def create_bool(tag):
	bool = f'bool_const_0:\n'
	bool += f'		.word	{tag}\n'
	bool += f'		.word	4\n'
	bool += f'		.word	Bool_disp\n'
	bool += f'		.word	0\n'
	bool += f'		.word	-1\n'
	bool += f'bool_const_1:\n'
	bool += f'		.word	{tag}\n'
	bool += f'		.word	4\n'
	bool += f'		.word	Bool_disp\n'
	bool += f'		.word	1\n'
	bool += f'		.word	-1\n'
	return bool

def create_disp(name, methods):
	disp = f'{name}_disp:\n'
	for meth in methods:
		disp += f'\t\t.word\t{meth.type}.{meth.name}\n'
	return disp

def create_proto(name, tag, attributes):
	proto = f'{name}_proto:\n'
	proto += f'		.word	{tag}\n'
	proto += f'		.word	{3 + len(attributes)}\n'
	proto += f'		.word	{name}_disp\n'
		
	for attr in attributes:
		if attr.type.name == 'Int' and name != 'Int':
			proto += f'		.word	int_const_0\n'
		elif attr.type.name == 'String' and name != 'String':
			proto += f'		.word	string_const_0\n'
		elif attr.type.name == 'Bool' and name != 'Bool':
			proto += f'		.word	bool_const_0\n'
		else:
			proto += f'		.word	0\n'
		
	proto += f'		.word	-1\n'
	return proto