from dataclasses import dataclass

from asts.ccil_ast import ExpressionNode
from typing import List
from __future__ import annotations


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
