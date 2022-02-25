from .formatter import *

coder = MIPSFormatter()
coder.label("Object_abort")
coder.load_int(V0, 55)
coder.move(A0, "ObjectErrorMessage")
coder.load_int(A1, 0)
coder.syscall()
coder.new_line()
coder.load_int(V0, 17)
coder.load_int(A0, 1)
coder.syscall()

OBJECT_ABORT = coder.code

coder.reset()

coder.label("Object_type_name")
coder.push(RA)
coder.push(FP)
coder.move(FP, SP)

coder.new_line()
coder.load_word(V7, '12($fp})')
coder.load_word(V6, '0($v7)')

coder.new_line()
coder.load_word(A0, '4($v6)')
coder.load_int(V0, 4)
coder.syscall()

coder.new_line()
coder.move(SP, FP)
coder.pop(FP)
coder.pop(RA)
coder.jump_return()

OBJECT_TYPE_NAME = coder.code

coder.reset()

coder.label("copy_Object")
coder.load_word(V7, '12($fp)')
coder.load_word(V6, '0($v7)')
coder.load_word(V5, '0($v6)')

coder.new_line()
coder.move(A0, V7)
coder.load_int(V0, 9)
coder.syscall()

coder.move(V6, V0)
coder.label("copy_Object_loop")
coder.load_word(V4, '0($v7)')
coder.save_word(V4, '0($v6)')
coder.addu(V7, V7, 4)
coder.addu(V6, V6, 4)
coder.addu(V5, V5, -4)
coder.bgtz(V5, "copy_Object_loop")
coder.jump_return()

OBJECT_COPY = coder.code

coder.reset()
coder.label("out_string_IO")
coder.load_word(A0, '12($fp)')
coder.move(V0, 4)
coder.syscall()
coder.jump_return()

IO_OUT_STRING = coder.code

coder.reset()
coder.label("out_int_IO")
coder.load_word(V1, '12($fp)')
coder.load_word(A0, '4($v1)')
coder.load_int(V0, 1)
coder.syscall()
coder.jump_return()

IO_OUT_INT = coder.code

coder.reset()
coder.label("strlen_String")
coder.load_word(A0, '12($fp)')



coder.label("in_string_IO")
coder.move(A0, "IO_Buffer")
coder.load_int(A1, 300)
coder.syscall()











