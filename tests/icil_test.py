
import pytest

import os
from utils import compare_outputs_icil

tests_dir = __file__.rpartition('/')[0] + '/initial_gen/'
tests_dir2 = __file__.rpartition('/')[0] + '/codegen/'
tests1 = [(file, tests_dir) for file in os.listdir(tests_dir) if file.endswith('.cl')]
tests2 = [(file, tests_dir2) for file in os.listdir(tests_dir2) if file.endswith('.cl')]

tests = tests1 + tests2

@pytest.mark.icil
@pytest.mark.ok
@pytest.mark.run(order=4)
@pytest.mark.parametrize("cool_files", tests)
def test_icil(main_path, cool_files):
    cool_file, tests_dir = cool_files
    compare_outputs_icil(main_path, tests_dir + cool_file, tests_dir + cool_file[:-3] + '_input.txt',\
        tests_dir + cool_file[:-3] + '_output.txt')

# if __name__ == "__main__":
#     pytest.main(["-m", "icil"])