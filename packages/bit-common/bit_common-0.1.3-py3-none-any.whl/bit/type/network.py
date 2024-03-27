import ipaddress
from typing import Union

from bit.type.integer import UnsignedInteger


class IPv4Address(UnsignedInteger):
    LENGTH = 32

    @classmethod
    def transform(cls, value: Union[str, int, list[int]]) -> int:
        if isinstance(value, str):
            return int(ipaddress.IPv4Address(value))

        return super().transform(value)


class IPv6Address(IPv4Address):
    LENGTH = 128

    @classmethod
    def transform(cls, value: Union[str, int, list[int]]) -> int:
        if isinstance(value, str):
            return int(ipaddress.IPv6Address(value))

        return super().transform(value)


class IPv4Mask(IPv4Address):
    pass


class IPv6Mask(IPv6Address):
    pass
