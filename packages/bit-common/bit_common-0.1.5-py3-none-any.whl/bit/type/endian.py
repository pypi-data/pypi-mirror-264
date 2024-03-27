import sys
import typing
from enum import Enum
from functools import wraps
from typing import Callable, Concatenate, ParamSpec, Union

if typing.TYPE_CHECKING:
    from bit.type.base import BaseType

P = ParamSpec("P")


class Endian(Enum):
    """Endianness."""

    LITTLE = "little"
    BIG = "big"


MACHINE_ENDIAN = Endian[sys.byteorder.upper()]


def _convert_endian(data: list[int]) -> list[int]:
    """Converts endianness of the data."""

    step = 8

    new_data = []

    for start in range(0, len(data), step):
        new_data += [data[start : start + step]]

    return [bit for byte in reversed(new_data) for bit in byte]


def convert_endian(data: list[int]) -> list[int]:
    """Converts endianness of the data."""

    if MACHINE_ENDIAN != Endian.LITTLE:
        return _convert_endian(data)

    return data


def convert_machine_endian(
    f: Callable[Concatenate[Union["BaseType", type["BaseType"]], P], list[int]]
) -> Callable[Concatenate[Union["BaseType", type["BaseType"]], P], list[int]]:
    """Converts endianness of the result bitarray to machine endian."""

    @wraps(f)
    def wrapper(
        data_type: Union["BaseType", type["BaseType"]],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> list[int]:
        return convert_endian(f(data_type, *args, **kwargs))

    return wrapper
