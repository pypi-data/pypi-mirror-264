from typing import Tuple, Type, Union
from typing_extensions import TypeAlias, TypeVarTuple, Unpack

from type_enum import TypeEnum

Ts = TypeVarTuple("Ts")

t: TypeAlias = Type[Tuple[Unpack[Ts]]]


class Color(TypeEnum):
    transparent: t[()]
    name: t[str, int]


T = Union[Color.transparent, Color.name]

tr = Color.transparent()
name = Color.name(("foo", 3))


def f(color: T) -> int:
    match color:
        case Color.transparent():
            return 0
        case Color.name(color_name):
            print(f"color name: {color_name}")
            return 0
