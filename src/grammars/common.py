# Basic terminals for common use

#
# Numbers
#

INT = r"\d+"
SIGNED_INT = r"[\+|\-]" + INT

#
# Strings
#
_STRING_INNER = r".*?"
_STRING_ESC_INNER = _STRING_INNER + r"(?<!\\)(\\\\)*?"
QUOTE = r"\""
STRING = QUOTE + _STRING_ESC_INNER + QUOTE

#
# Names (Variables)
#
L_CASE_LETTER = r"[a-z]"
U_CASE_LETTER = r"[A-Z]"

LETTER = r"[a-zA-Z]"
WORD = r"[a-zA-Z]+"

VAR_NAME = r"[a-z][a-zA-Z0-9_]*"
TYPE_NAME = r"[A-Z][a-zA-Z0-9_]*"

#
# Whitespace
#
WS_INLINE = r"[ \t\v\f\r]"

CR = r"\r"
LF = r"\n"
NEWLINE = r"\n+"

#
# Comments
#
INLINE_COMMENT = r"--[^\n]*"
OPEN_BLOCK_COMMENT = r"\(\*"
CLOSE_BLOCK_COMMENT = r"\*\)"