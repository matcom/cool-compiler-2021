from dataclasses import dataclass

from asts.ccil_ast import ExpressionNode
from typing import Dict, List, Tuple
from __future__ import annotations


class Scope:
    def __init__(self, parent: Scope = None):
        self.children: List[Scope] = []
        self.names: Dict[str, str] = dict()
        self.parent = parent

    @property
    def get_parent(self):
        if self.parent is None:
            raise Exception("Scope parent is None")

        return self.parent

    def create_child(self):
        self.children.append(Scope())
        return self.children[-1]

    def add_new_name_pair(self, key: str, value: str):
        if key in self.names:
            raise Exception(
                f"Re inserting {key} with {value}."
                f" Value to be replaced is {self.names[key]}"
            )
        self.names[key] = value

    def add_new_names(self, *names: List[Tuple[str, str]]):
        for (k, v) in names:
            self.add_new_name_pair(k, v)

    def search_value(self, key: str) -> str | None:
        (key, _) = self.search_value_position(key)
        return key

    def search_value_position(self, key: str) -> Tuple[str, bool] | Tuple[None, None]:
        try:
            return (self.names[key], self.parent is None)
        except KeyError:
            return (
                self.parent.search_for(key) if self.parent is not None else (None, None)
            )

    def get_value_position(self, key: str) -> Tuple[str, bool]:
        result = self.search_value_position(key)
        if any(map(lambda x: x is None, result)):
            raise Exception(f"{key} cannot be found")

        return result
