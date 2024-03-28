from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Type
from typing_extensions import TypeAlias, TypeVarTuple, Unpack

_Ts = TypeVarTuple("_Ts")

Field: TypeAlias = Type[Tuple[Unpack[_Ts]]]


@dataclass
class A:
    y: Field[C]


class C: ...
