
import pytest

import os
from utils import compare_outputs

tests_dir = __file__.rpartition('/')[0] + '/initial_gen/'
tests = [(file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.initial_gen
@pytest.mark.ok
@pytest.mark.run(order=4)
@pytest.mark.parametrize("cool_file", tests)
def test_initial_gen(compiler_path, cool_file):
    compare_outputs(compiler_path, tests_dir + cool_file, tests_dir + cool_file[:-3] + '_input.txt',\
        tests_dir + cool_file[:-3] + '_output.txt')
    