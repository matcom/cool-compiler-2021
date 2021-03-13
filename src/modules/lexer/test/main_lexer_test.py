import pytest
import os

tests_dir = __file__.rpartition("/")[0] + "/input/iis/"
tests = [(file) for file in os.listdir(tests_dir) if file.endswith(".cl")]

from src.modules.lexer import CoolLexer


@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=1)
def test_iis():
    for test in tests:
        fd = open(tests_dir + test)
        code = fd.read()
        lexer = CoolLexer(lexer_errors=[])
        for token in lexer.tokenize(code):
            print(token)
        fd2 = open(tests_dir + test[:-3] + "_error.txt")
        errors = fd2.read().split("\n")
        assert lexer.errors == errors
