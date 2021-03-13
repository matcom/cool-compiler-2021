import pytest
import os

tests_dir = __file__.rpartition("/")[0] + "/input/comments/"
tests = [(file) for file in os.listdir(tests_dir) if file.endswith(".cl")]

from src.modules.lexer import CoolLexer


@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=2)
def test_should_eof_in_comment():
    for test in tests:
        fd = open(tests_dir + test)
        code = fd.read()
        lexer = CoolLexer(lexer_errors=[])
        for token in lexer.tokenize(code):
            pass
        assert lexer.errors == ["(55, 46) - LexicographicError: EOF in comment"]
