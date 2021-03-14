import pytest
import os

tests_dir = __file__.rpartition("/")[0] + "/input/mixed/"

from .utils import compare_results


@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=4)
def test_mixed():
    compare_results(tests_dir)
