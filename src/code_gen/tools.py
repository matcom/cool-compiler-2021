from __future__ import annotations
from dataclasses import dataclass

from typing import List


@dataclass(frozen=True)
class Class:
    attributes: List[Attribute]
    methods: List[Method]


@dataclass(frozen=True)
class Attribute:
    id: str
    type: str


@dataclass(frozen=True)
class Method:
    id: str
