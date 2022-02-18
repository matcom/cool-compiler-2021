
import pytest

import os
from utils import compare_outputs_icil

tests_dir = __file__.rpartition('/')[0] + '/initial_gen/'
tests = [(file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.icil
@pytest.mark.ok
@pytest.mark.run(order=6)
@pytest.mark.parametrize("cool_file", tests)
def test_icil(compiler_path, cool_file):
    compare_outputs_icil(compiler_path, tests_dir + cool_file, tests_dir + cool_file[:-3] + '_input.txt',\
        tests_dir + cool_file[:-3] + '_output.txt')