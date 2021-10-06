from typing import Text
from MIPS.ast import *

def add_string(name, tag, int_const, value):
	string = f'{name}:\n'
	string += f'		.word	{tag}\n'
	string += f'		.word	6\n'
	string += f'		.word	String_disp\n'
	string += f'		.word	{int_const}\n'
	string += f'		.ascii	"{value}"\n'
	string += f'		.byte	0\n'
	string += f'		.word	-1\n'
	return string

def add_int(name, tag, value):
	integer = f'{name}:\n'
	integer += f'		.word	{tag}\n'
	integer += f'		.word	4\n'
	integer += f'		.word	Int_disp\n'
	integer += f'		.word	{value}\n'
	integer += f'		.word	-1\n'
	return integer

def add_bool(tag, value):
	bool = f'bool_const_{value}:\n'
	bool += f'		.word	{tag}\n'
	bool += f'		.word	4\n'
	bool += f'		.word	Bool_disp\n'
	bool += f'		.word	{value}\n'
	bool += f'		.word	-1\n'
	return bool

def create_object_item(name):
	item_tab = f'		.word	{name}_proto\n'
	item_tab += f'		.word	{name}_init\n'
	return item_tab

def create_name_item(name):
	return f'		.word	{name}\n'

def create_proto(name, tag, attrs):
	proto = f'{name}_proto:\n'
	proto += f'		.word	{tag}\n'
	proto += f'		.word	{3 + len(attrs)}\n'
	proto += f'		.word	{name}_disp\n'
		
	for attr in attrs:
		if attr[1].name == 'Int' and name != 'Int':
			proto += f'		.word	int_const_0\n'
		elif attr[1].name == 'String' and name != 'String':
			proto += f'		.word	string_const_0\n'
		elif attr[1].name == 'Bool' and name != 'Bool':
			proto += f'		.word	bool_const_0\n'
		else:
			proto += f'		.word	0\n'
		
	proto += f'		.word	-1\n'
	return proto

def create_disp(name, methds):
	disp = f'{name}_disp:\n'
	for meth in methds:
		disp += f'		.word	{meth[1]}_{meth[0]}\n'
	return disp

def call_methodo(name, int_tex):
	text  = f'{name}:\n'
	text += f'		addiu   $sp -12\n'
	text += f'		sw      $fp 12($sp)\n'
	text += f'		sw      $s0 8($sp)\n'
	text += f'		sw      $ra 4($sp)\n'
	text += int_tex
	text += f'		lw      $fp 12($sp)\n'
	text += f'		lw      $s0 8($sp)\n'
	text += f'		lw      $ra 4($sp)\n'
	text += f'		addiu   $sp $sp 12\n'
	text += f'		jr      $ra\n'
	return text

def create_init(name, int_text, parent='Object'):
	text  = f'{name}:\n'
	text += f'		addiu   $sp -12\n'
	text += f'		sw      $fp 12($sp)\n'
	text += f'		sw      $s0 8($sp)\n'
	text += f'		sw      $ra 4($sp)\n'
	#text += f'		jal     {parent}_init\n'
	text += int_text
	text += f'		move    $a0 $s0\n'
	text += f'		lw      $fp 12($sp)\n'
	text += f'		lw      $s0 8($sp)\n'
	text += f'		lw      $ra 4($sp)\n'
	text += f'		addiu   $sp $sp 12\n'
	text += f'		jr      $ra\n'
	return text

exceptions='''
_abort_msg:	    .asciiz "Abort called from class "
_colon_msg:	    .asciiz ":"
_dispatch_msg:  .asciiz ": Dispatch to void.\\n"
_cabort_msg:	.asciiz "No match in case statement for Class "
_cabort_msg2:   .asciiz "Match on void in case statement.\\n"
_nl:		    .asciiz "\\n"
_term_msg:	    .asciiz "COOL program successfully executed\\n"
_sabort_msg1:	.asciiz	"Index to substr is negative\\n"
_sabort_msg2:	.asciiz	"Index to substr is too big\\n"
_sabort_msg3:	.asciiz	"Length to substr too long\\n"
_sabort_msg4:	.asciiz	"Length to substr is negative\\n"
_sabort_msg:	.asciiz "Execution aborted.\\n"
_objcopy_msg:	.asciiz "Object.copy: Invalid object size.\\n"
_gc_abort_msg:	.asciiz "GC bug!\\n"
'''

all_init = '''Object_init:
		addiu   $sp $sp -12
		sw		$fp 12($sp)
		sw		$s0 8($sp)
		sw		$ra 4($sp)
		addiu	$fp $sp 4
		move	$s0 $a0
		move	$a0 $s0
		lw		$fp 12($sp)
		lw		$s0 8($sp)
		lw		$ra 4($sp)
		addiu	$sp $sp 12
		jr	$ra
IO_init:
		addiu	$sp $sp -12
		sw		$fp 12($sp)
		sw		$s0 8($sp)
		sw		$ra 4($sp)
		addiu	$fp $sp 4
		move	$s0 $a0
		jal		Object_init
		move	$a0 $s0
		lw		$fp 12($sp)
		lw		$s0 8($sp)
		lw		$ra 4($sp)
		addiu	$sp $sp 12
		jr	$ra	
Int_init:
		addiu	$sp $sp -12
		sw		$fp 12($sp)
		sw		$s0 8($sp)
		sw		$ra 4($sp)
		addiu	$fp $sp 4
		move	$s0 $a0
		jal		Object_init
		move	$a0 $s0
		lw		$fp 12($sp)
		lw		$s0 8($sp)
		lw		$ra 4($sp)
		addiu	$sp $sp 12
		jr	$ra
String_init:
		addiu	$sp $sp -12
		sw		$fp 12($sp)
		sw		$s0 8($sp)
		sw		$ra 4($sp)
		addiu	$fp $sp 4
		move	$s0 $a0
		jal		Object_init
		move	$a0 $s0
		lw		$fp 12($sp)
		lw		$s0 8($sp)
		lw		$ra 4($sp)
		addiu	$sp $sp 12
		jr		$ra	
Bool_init:
		addiu	$sp $sp -12
		sw		$fp 12($sp)
		sw		$s0 8($sp)
		sw		$ra 4($sp)
		addiu	$fp $sp 4
		move	$s0 $a0
		jal		Object_init
		move	$a0 $s0
		lw		$fp 12($sp)
		lw		$s0 8($sp)
		lw		$ra 4($sp)
		addiu	$sp $sp 12
		jr		$ra	
'''

main = '''main:
		la		$a0 Main_proto		# create the Main object
		jal		Object.copy			# Call copy
		
		move	$s0 $v0
		
		jal		Main_init			# initialize the Main object
		jal		Main.main			# Invoke main method
		
		li 		$v0 10
		syscall						# syscall 10 (exit)
'''

basic_build = '''
Object.copy:
		addiu	$sp $sp -8			# create stack frame
		sw		$ra 8($sp)			# save $ra in stack 
		sw		$a0 4($sp)			# save proto in stack

		lw		$a0 4($sp)			
		jal		object_copy_allocate
		
		addiu	$gp $gp 4			# add 4 for new object

		lw		$a0 4($sp)			# the self object
		lw		$ra 8($sp)			# restore return address
		addiu	$sp $sp 8			# remove frame

		jr		$ra					# return

object_copy_allocate:
		addiu	$sp $sp -8			
		sw		$ra 8($sp)			# save ra
		sw		$gp 4($sp)			# save gp
		
		lw		$t1 4($a0)			# get object size
while:
		beq		$0 $t1	end_while	# if t1 == 0 jump 
		
		lw		$t0	0($a0)
		sw		$t0 0($gp)

		addiu	$gp $gp	4
		addiu	$a0 $a0	4

		addiu	$t1 $t1	-1
		jal		while
end_while:

		li		$t0 -1				
		sw		$t0	0($gp)			# add -1 on end

		lw		$v0 4($sp)			# get ra
		lw		$ra 8($sp)			# get ra
		addiu	$sp $sp 8 			
		
		jr		$ra					# return
'''