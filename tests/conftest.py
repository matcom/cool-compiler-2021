import pytest
import os

@pytest.fixture
def compiler_path():
	# return os.path.abspath('./src/coolc.sh')
	return os.path.abspath(os.path.join('src', 'coolc.sh'))
