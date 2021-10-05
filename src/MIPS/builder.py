from MIPS.ast import *

def exceptions():
    return '''
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