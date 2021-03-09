import pytest
import os

@pytest.fixture
def compiler_path():
	if os.getcwd().endswith('src'):
		return os.path.abspath('./coolc.sh')
	
	# For local test using the testing system of visual studio code
	return os.path.abspath(os.path.join('src', 'coolc.sh'))
