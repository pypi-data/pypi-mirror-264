from typing import (
    Annotated,
    Any,
    Callable,
    ClassVar,
    Optional,
    ParamSpec,
    Self,
    Union,
    cast,
    get_args,
    get_origin,
)

import pydantic
from mypy.types import JsonDict
from pydantic import Field
from pydantic.fields import FieldInfo

from bit.type.base import BaseType
from bit.type.bitarray import BitArray

P = ParamSpec("P")


class DynamicType(pydantic.BaseModel):
    """Model for settings dynamic field type by reference to other field."""

    getter: Annotated[
        Callable[[type["BaseModel"]], BaseType],
        Field(description="Getter function to get the type."),
    ]

    field: Annotated[
        str,
        Field(description="Field to get the argument from."),
    ]


class BitSchemaExtra:
    """Extra schema data with references to other fields and helpers for binary conversion."""

    def __init__(
        self,
        length_field_name: Optional[str] = None,
        dynamic_type: Optional[DynamicType] = None,
        compute_on_to_bits: Callable[["BaseModel"], Any] | None = None,
        exclude_from_bits: bool = False,
        **kwargs: P.args,
    ):
        """Additional bit schema data placed in the field metadata.

        :param length_field_name: Length field for list fields.
        :param dynamic_type: Dynamic type getter.
        :param compute_on_to_bits: Uses a function to compute the field on output.
        :param exclude_from_bits: Exclude this field from the bitarray.
        :param kwargs: Additional arguments.
        """

        self.length_field_name = length_field_name
        self.dynamic_type = dynamic_type
        self.compute_on_to_bits = compute_on_to_bits
        self.exclude_from_bitarray = exclude_from_bits
        self.kwargs = kwargs

    @classmethod
    def find(cls, metadata: list[Any | Self]) -> Self:
        """Finds the extra metadata in the field metadata."""

        for item in metadata:
            if isinstance(item, cls):
                return item

        return cls()


class BaseModel(pydantic.BaseModel):
    REORDER: ClassVar[list[str]]
    """Reorder fields in the model conversion from bits and to bits."""

    def to_bits(self, exclude: Optional[set[str]] = None) -> BitArray:
        """Converts the object to a bitarray."""

        data = BitArray()

        model_data = self.model_dump(exclude=exclude)

        order = self.REORDER or model_data.keys()  # noqa: undefined-variable

        for field_name in order:
            value = getattr(self, field_name)
            field = self.__fields__[field_name]
            extra = BitSchemaExtra.find(field.metadata)

            if extra.compute_on_to_bits is not None:
                value = extra.compute_on_to_bits(self)

            if extra.exclude_from_bitarray:
                continue

            if isinstance(value, list):
                for item in value:
                    data.write(item.to_bits())
            elif isinstance(value, BaseType):
                data.write(value.to_bits())
            elif isinstance(value, BaseModel):
                data.write(value.to_bits())
            else:
                raise ValueError(f"Invalid type {type(value)} for field {field_name}")

        return data

    @classmethod
    def _field_from_bits(
        cls,
        field_type: type[BaseType],
        bitarray: BitArray,
        ctx: JsonDict | Callable[[JsonDict], None] | None = None,
    ) -> BaseType:
        """Parses a field from a bitarray."""

        pos_backup = bitarray.pos

        if get_origin(field_type) is Union:
            for inner_type in get_args(field_type):
                try:
                    return cast(BaseType, inner_type.from_bits(bitarray, ctx=ctx))
                except ValueError:
                    bitarray.pos = pos_backup
            else:
                raise ValueError("No valid type found")

        else:
            return field_type.from_bits(bitarray, ctx=ctx)

    @classmethod
    def _get_type(
        cls,
        field: FieldInfo,
        data: dict[str, Any],
        metadata: list[Any | BitSchemaExtra],
    ) -> BaseType:
        """Get the type for a given data."""

        extra = BitSchemaExtra.find(metadata)

        if extra.dynamic_type is not None:
            return extra.dynamic_type.getter(data[extra.dynamic_type.field])

        return cast(BaseType, field.annotation)

    @classmethod
    def from_bits(
        cls,
        bitarray: BitArray | list[int],
        ctx: JsonDict | Callable[[JsonDict], None] | None = None,
    ) -> Self:
        """Parses a DNS header from a bitarray."""

        if isinstance(bitarray, list):
            bitarray = BitArray.from_bits(bitarray)

        data: dict[str, Any] = {}
        order = (
            cls.REORDER
            or cls.model_json_schema(
                mode="serialization",
                by_alias=False,
            )["properties"].keys()
        )

        for field_name in order:
            field = cls.model_fields[field_name]  # noqa: unresolved-reference
            field_type = cast(
                type[BaseType],
                cls._get_type(field, data, field.metadata),
            )
            field_name = field.alias or field_name
            schema_extra = BitSchemaExtra.find(field.metadata)

            if schema_extra.exclude_from_bitarray:
                continue

            # Optional fields are present as Union with None with real type as first argument
            if get_origin(field_type) is Union and type(None) in get_args(field_type):
                field_type = get_args(field_type)[0]

            # List fields are present as List with real type as first argument
            if get_origin(field_type) is list and schema_extra.length_field_name is not None:
                inner_type = get_args(field_type)[0]

                list_length = data[schema_extra.length_field_name].value

                data[field_name] = [
                    cls._field_from_bits(
                        inner_type,
                        bitarray,
                        ctx=field.json_schema_extra,
                    )
                    for _ in range(list_length)
                ]

            elif get_origin(field_type) is list and schema_extra.length_field_name is None:
                raise ValueError("List field without length field")

            else:
                data[field_name] = cls._field_from_bits(
                    field_type,
                    bitarray,
                    ctx=field.json_schema_extra,
                )

        return cls(**data)
