import pytest
import os

@pytest.fixture
def compiler_path():
	curr = os.path.dirname(__file__)
	return os.path.join(curr, "..", "src", 'coolc.sh')
	# return os.path.abspath('./coolc.sh')