from typing import Any, ClassVar, Self, Union, cast

from pydantic.json_schema import (  # type: ignore[attr-defined]
    GetJsonSchemaHandler,
    JsonSchemaValue,
)
from pydantic_core import core_schema

from bit.type.base import BaseType
from bit.type.bitarray import BitArray
from bit.type.endian import Endian


class Integer(BaseType):
    ENDIAN: ClassVar[Endian] = Endian.BIG
    SIGNED: bool = True
    EXTRA: ClassVar[type] = int

    @classmethod
    def _get_core_schema(cls) -> core_schema.IntSchema:  # type: ignore[override]
        return core_schema.int_schema(
            ge=cls.min_value(),
            le=cls.max_value(),
            strict=True,
            ref=cls.__name__,
        )

    @classmethod
    def max_value(cls) -> int:
        length = cast(int, cls.LENGTH)
        return int(2 ** (length - 1) - 1 if cls.SIGNED else 2**length - 1)

    @classmethod
    def min_value(cls) -> int:
        length = cast(int, cls.LENGTH)
        return int(-(2 ** (length - 1)) if cls.SIGNED else 0)

    @classmethod
    def from_bits(cls, bits: Union[BitArray, list[int]], **kwargs) -> Self:  # type: ignore
        """Converts list of bits to integer."""

        if isinstance(bits, list):
            bits = BitArray.from_bits(bits)

        return cls(sum([2**i * v for i, v in enumerate(cls._read_bits(bits))]))

    def _to_bits(self) -> list[int]:
        """Converts integer to list of bits."""

        length = cast(int, self.LENGTH)

        if not self.SIGNED:
            return [(self.value >> i) & 1 for i in range(length)]
        else:
            return [(self.value >> i) & 1 for i in range(length - 1)] + [int(self.value < 0)]

    @classmethod
    def transform(cls, value: Union[bool, int, list[int], Any]) -> int:
        """Converts value to integer."""

        if isinstance(value, bool):
            return int(value)

        if isinstance(value, list):
            if len(value) != cls.LENGTH:
                raise ValueError(f"Expected {cls.LENGTH} bits, got {len(value)}.")

            if any(bit not in (0, 1) for bit in value):
                raise ValueError("Expected 0 or 1.")

            return sum([2**i * v for i, v in enumerate(reversed(value))])

        return int(super().transform(value))

    @classmethod
    def _validate(
        cls,
        value: Union[int, list[int], Self],
        info: dict[str, Any] | core_schema.ValidationInfo,
    ) -> int:
        """Validates a value."""

        if isinstance(value, bool):
            return int(value)

        if isinstance(value, list):
            if len(value) != cls.LENGTH:
                raise ValueError(f"Expected {cls.LENGTH} bits, got {len(value)}.")

            if any(bit not in (0, 1) for bit in value):
                raise ValueError("Expected 0 or 1.")

            return sum([2**i * v for i, v in enumerate(reversed(value))])

        elif isinstance(value, int):
            if not cls.min_value() <= value <= cls.max_value():
                raise ValueError(
                    f"Expected {cls.min_value()} <= value <= {cls.max_value()}, got {value}."
                )
            return value

        elif isinstance(value, Integer):
            return int(value.value)

        else:
            raise ValueError(f"Expected int or list of bits, got {type(value)}.")

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: core_schema.JsonSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """Returns JSON schema for integer."""

        return {
            "type": "integer",
            "minimum": cls.min_value(),
            "maximum": cls.max_value(),
        }

    def __repr__(self) -> str:
        return f"{self.value}"


class UnsignedInteger(Integer):
    SIGNED = False


class Boolean(UnsignedInteger):
    LENGTH: ClassVar[int] = 1
    EXTRA: ClassVar[type] = bool

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "boolean"}

    @classmethod
    def _validate(
        cls,
        value: Union[int, list[int], bool, Self],
        info: dict[str, Any] | core_schema.ValidationInfo,
    ) -> int:
        if isinstance(value, bool):
            return value

        if isinstance(value, cls):
            return int(value.value)

        return super()._validate(value, info)


def _generate_int_type(int_length: int, int_type: type[Integer]) -> type[Integer]:
    return cast(type[Integer], type(f"int{int_length}", (int_type,), {"LENGTH": int_length}))


# Generate integer type
int1 = _generate_int_type(1, Integer)
int2 = _generate_int_type(2, Integer)
int3 = _generate_int_type(3, Integer)
int4 = _generate_int_type(4, Integer)
int8 = _generate_int_type(8, Integer)
int16 = _generate_int_type(16, Integer)
int32 = _generate_int_type(32, Integer)
int64 = _generate_int_type(64, Integer)
int128 = _generate_int_type(128, Integer)


# Generate unsigned integer type
uint1 = _generate_int_type(1, UnsignedInteger)
uint2 = _generate_int_type(2, UnsignedInteger)
uint3 = _generate_int_type(3, UnsignedInteger)
uint4 = _generate_int_type(4, UnsignedInteger)
uint8 = _generate_int_type(8, UnsignedInteger)
uint16 = _generate_int_type(16, UnsignedInteger)
uint32 = _generate_int_type(32, UnsignedInteger)
uint64 = _generate_int_type(64, UnsignedInteger)
uint128 = _generate_int_type(128, UnsignedInteger)


# Generate special type
boolean = _generate_int_type(1, Boolean)
