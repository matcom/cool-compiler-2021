import pytest
import os

tests_dir = __file__.rpartition("/")[0] + "/input/comments/"

from .utils import compare_results


@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=2)
def test_should_eof_in_comment():
    compare_results(tests_dir)
