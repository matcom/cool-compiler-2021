import pytest
import os

tests_dir = __file__.rpartition("/")[0] + "/input/iis/"

from src.modules.lexer import CoolLexer
from .utils import compare_results


@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=1)
def test_iis():
    compare_results(tests_dir)
