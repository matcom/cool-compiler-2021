	.data
data_0: .asciiz "Abort called from class "
data_1: .asciiz ""
data_2: .asciiz "Substring out of range"
data_3: .asciiz "Hello, World."
data_4: .asciiz "(3, 2) - RuntimeError: Dispatch on void"

type_list:
	.word	Object
	.word	IO
	.word	String
	.word	Int
	.word	Bool
	.word	Main

virtual_table:
	.word	Object_proto
	.word	IO_proto
	.word	String_proto
	.word	Int_proto
	.word	Bool_proto
	.word	Main_proto

Object_dispatch:
	.word	 function_abort_at_Object
	.word	 function_type_name_at_Object
	.word	 function_copy_at_Object
	.word	 init_at_Object

Object_proto:
	.word	0
	.word	0
	.word	Object_dispatch
	.word	-1

IO_dispatch:
	.word	 function_abort_at_Object
	.word	 function_type_name_at_Object
	.word	 function_copy_at_Object
	.word	 function_out_string_at_IO
	.word	 function_out_int_at_IO
	.word	 function_in_string_at_IO
	.word	 function_in_int_at_IO
	.word	 init_at_IO

IO_proto:
	.word	1
	.word	0
	.word	IO_dispatch
	.word	-1

String_dispatch:
	.word	 function_abort_at_Object
	.word	 function_type_name_at_Object
	.word	 function_copy_at_Object
	.word	 function_length_at_String
	.word	 function_concat_at_String
	.word	 function_substr_at_String
	.word	 init_at_String

String_proto:
	.word	2
	.word	8
	.word	String_dispatch
	.word	0
	.word	0
	.word	-1

Int_dispatch:
	.word	 function_abort_at_Object
	.word	 function_type_name_at_Object
	.word	 function_copy_at_Object
	.word	 init_at_Int

Int_proto:
	.word	3
	.word	4
	.word	Int_dispatch
	.word	0
	.word	-1

Bool_dispatch:
	.word	 function_abort_at_Object
	.word	 function_type_name_at_Object
	.word	 function_copy_at_Object
	.word	 init_at_Bool

Bool_proto:
	.word	4
	.word	4
	.word	Bool_dispatch
	.word	0
	.word	-1

Main_dispatch:
	.word	 function_abort_at_Object
	.word	 function_type_name_at_Object
	.word	 function_copy_at_Object
	.word	 function_out_string_at_IO
	.word	 function_out_int_at_IO
	.word	 function_in_string_at_IO
	.word	 function_in_int_at_IO
	.word	 function_main_at_Main

Main_proto:
	.word	5
	.word	0
	.word	Main_dispatch
	.word	-1
	.text
	.globl main
entry:
	
init_at_Object:
	
function_abort_at_Object:
	
function_type_name_at_Object:
	
function_copy_at_Object:
	
init_at_IO:
	
function_out_string_at_IO:
	
function_out_int_at_IO:
	
function_in_string_at_IO:
	
function_in_int_at_IO:
	
init_at_String:
	
function_length_at_String:
	
function_concat_at_String:
	
function_substr_at_String:
	
init_at_Int:
	
init_at_Bool:
	
function_main_at_Main:
	
init_at_Main:
	
init_attr_at_Main:
	
