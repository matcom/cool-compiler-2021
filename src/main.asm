.data
	type_Object: .word 4
	type_Object_inherits_from: .word 0
	type_Object_attributes: .word 0
	type_Object_name: .asciiz "Object"
	
	type_IO: .word 4
	type_IO_inherits_from: .word type_Object
	type_IO_attributes: .word 0
	type_IO_name: .asciiz "IO"
	
	type_Int: .word 4
	type_Int_inherits_from: .word type_Object
	type_Int_attributes: .word 0
	type_Int_name: .asciiz "Int"
	
	type_String: .word 4
	type_String_inherits_from: .word type_Object
	type_String_attributes: .word 0
	type_String_name: .asciiz "String"
	
	type_Bool: .word 4
	type_Bool_inherits_from: .word type_Object
	type_Bool_attributes: .word 0
	type_Bool_name: .asciiz "Bool"
	
	type_Main: .word 8
	type_Main_inherits_from: .word type_IO
	type_Main_attributes: .word 1
	type_Main_name: .asciiz "Main"
	

.text
	function___init___at_Object:
		jr $ra
		
	function_abort_at_Object:
		jr $ra
		
	function_type_name_at_Object:
		jr $ra
		
	function_copy_at_Object:
		jr $ra
		
	function___init___at_IO:
		jr $ra
		
	function_out_string_at_IO:
		jr $ra
		
	function_out_int_at_IO:
		jr $ra
		
	function_in_string_at_IO:
		jr $ra
		
	function_in_int_at_IO:
		jr $ra
		
	function___init___at_S:
		jr $ra
		
	function_length_at_String:
		jr $ra
		
	function_concat_at_String:
		jr $ra
		
	function_substr_at_String:
		jr $ra
		
	function___init___at_Main:
		jr $ra
		
	function_main_at_Main:
		jr $ra
		
	main: