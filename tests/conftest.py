import pytest
import os
import platform


@pytest.fixture
def compiler_path():
	extension = 'sh' if platform.system() != 'Windows' else 'py'

	if os.getcwd().endswith('src'):
		return os.path.abspath(f'./coolc.{extension}')
	
	# For local test using the testing system of visual studio code
	return os.path.abspath(os.path.join('src', f'coolc.{extension}'))
