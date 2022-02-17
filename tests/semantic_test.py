import pytest
import pathlib
import os
from .utils import compare_errors, first_error_only_line

tests_dir = str(pathlib.Path(__file__).parent / 'semantic/')
#tests_dir = __file__.rpartition('/')[0] + '/semantic/'
try:
    tests = [(file) for file in os.listdir(tests_dir) if file.endswith('.cl')]
except:pass
@pytest.mark.semantic
@pytest.mark.error
@pytest.mark.run(order=3)
@pytest.mark.parametrize("cool_file", tests)
def test_semantic_errors(compiler_path, cool_file):
    # compare_errors(compiler_path, tests_dir + cool_file, tests_dir + cool_file[:-3] + '_error.txt', \
    #     cmp=first_error_only_line)
    compare_errors(compiler_path, str(os.path.join(tests_dir, cool_file)),\
            str(os.path.join(tests_dir, cool_file[:-3] + '_error.txt')),\
            cmp=first_error_only_line)