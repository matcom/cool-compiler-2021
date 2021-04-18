"""
Cool pipes package
"""

from typing import List
from cool_cmp.shared.pipeline.pipes import *

class IPipeable:

    @property
    def name(self)->str:
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
