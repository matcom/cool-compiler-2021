import pytest
import os

tests_dir = __file__.rpartition("/")[0] + "/input/strings/"

from .utils import compare_results


@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=3)
def test_string_errors():
    compare_results(tests_dir)
