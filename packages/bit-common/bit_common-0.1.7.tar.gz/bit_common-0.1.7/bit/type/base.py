from abc import abstractmethod
from typing import Any, Callable, ClassVar, Optional, Self, Union, cast

from mypy.types import JsonDict
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

from bit.type.bitarray import BitArray
from bit.type.endian import Endian, convert_machine_endian

UNDEFINED = object()


class BaseType:
    LENGTH: ClassVar[object | int] = UNDEFINED  # Length in bits
    ENDIAN: ClassVar[Endian] = Endian.LITTLE  # Network endianness
    EXTRA: ClassVar[type]  # Built-in type

    def __init__(self, value: Any):
        """Initializes the object."""

        # Transform and validate the value
        value = self.transform(value)
        self.validate(value, self._get_core_schema())

        self.value = value

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "value":
            value = self.transform(value)
            self.validate(value, self._get_core_schema())
        super().__setattr__(key, value)

    @classmethod
    def transform(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value.value
        return value

    @classmethod  # type: ignore[arg-type]
    @convert_machine_endian
    def _read_bits(cls, /, data: BitArray, length: Optional[int] = None) -> list[int]:
        return data.read(length or cast(int, cls.LENGTH))

    @classmethod  # type: ignore[arg-type]
    @convert_machine_endian
    def _peek_bits(
        cls,
        /,
        data: BitArray,
        length: int | None = None,
        offset: int = 0,
    ) -> list[int]:
        return data.peek(length or cast(int, cls.LENGTH), offset)

    @classmethod
    def _read_bytes(cls, data: BitArray, length: int) -> bytearray:
        return data.read_bytes(length)

    @classmethod
    def peek(cls, data: BitArray) -> Self:
        """Peek at next bits. Keep position unchanged."""

        return cls.from_bits(BitArray.from_bits(cls._peek_bits(data)))

    @classmethod
    @abstractmethod
    def from_bits(
        cls,
        data: Union[BitArray, list[int]],
        ctx: JsonDict | Callable[[JsonDict], None] | None = None,
    ) -> Self:
        """Parses a value from a bitarray."""

    @convert_machine_endian  # type: ignore[arg-type]
    def to_bits(self) -> list[int]:
        """Converts the object to a bitarray."""

        return self._to_bits()

    @abstractmethod
    def _to_bits(self) -> list[int]:
        """Inner method to convert value to bits."""

    @classmethod
    @abstractmethod
    def _validate(cls, value: Any, info: dict[str, Any] | core_schema.ValidationInfo) -> Any:
        """Validates a value."""

    @classmethod
    def validate(cls, value: Any, info: dict[str, Any] | core_schema.ValidationInfo) -> Any:
        """Validates a value."""

        if isinstance(value, cls):
            return value

        return cls._validate(value, info)

    @classmethod
    @abstractmethod
    def _get_core_schema(cls) -> dict[str, Any]:
        pass

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.PlainValidatorFunctionSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate,
            metadata=cls._get_core_schema(),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __hash__(self) -> int:
        return hash(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self, other: Any | Self) -> bool:
        if isinstance(other, self.__class__):
            return bool(self.value == other.value)
        return bool(self.value == other)

    def __ne__(self, other: Any | Self) -> bool:
        if isinstance(other, self.__class__):
            return bool(self.value != other.value)
        return bool(self.value != other)

    def __lt__(self, other: Any | Self) -> bool:
        if isinstance(other, self.__class__):
            return bool(self.value < other.value)
        return bool(self.value < other)

    def __le__(self, other: Any | Self) -> bool:
        if isinstance(other, self.__class__):
            return bool(self.value <= other.value)
        return bool(self.value <= other)

    def __gt__(self, other: Any | Self) -> bool:
        if isinstance(other, self.__class__):
            return bool(self.value > other.value)
        return bool(self.value > other)

    def __ge__(self, other: Any | Self) -> bool:
        if isinstance(other, self.__class__):
            return bool(self.value >= other.value)
        return bool(self.value >= other)

    def __add__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value + other.value)
        return self.__class__(self.value + other)

    def __sub__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value - other.value)
        return self.__class__(self.value - other)

    def __mul__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value * other.value)
        return self.__class__(self.value * other)

    def __truediv__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value / other.value)
        return self.__class__(self.value / other)

    def __floordiv__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value // other.value)
        return self.__class__(self.value // other)

    def __mod__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value % other.value)
        return self.__class__(self.value % other)

    def __pow__(self, other: Any | Self) -> Self:
        if isinstance(other, self.__class__):
            return self.__class__(self.value**other.value)
        return self.__class__(self.value**other)
