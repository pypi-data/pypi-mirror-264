from __future__ import annotations
from typing import Tuple, Type

from type_enum import TypeEnum

c: C


class C: ...


class Color(TypeEnum):
    transparent: Type[Tuple[()]]
    name: Type[Tuple[str]]


def f(color: Color.T) -> int:
    match color:
        case Color.transparent():
            return 0
        case Color.name(color_name):
            print(f"color name: {color_name}")
            return 0
