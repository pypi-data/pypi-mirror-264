import copy
from typing import Self, Union


class BitArray:
    """Array of bits. Which is a list of 0s and 1s.

    Array of data is always big-endian.
    """

    def __init__(self, data: bytearray | bytes | None = None):
        self.data = self.bytes_to_bits(bytearray(data or b""))
        self.pos = 0

    @staticmethod
    def bytes_to_bits(data: Union[bytes, bytearray]) -> list[int]:
        """Converts bytes to list of individual bits."""

        bits = []

        for byte in data:
            for i in range(0, 8):
                bits.append((byte >> i) & 1)

        return bits

    @staticmethod
    def bits_to_bytes(bits: Union["BitArray", list[int]]) -> bytearray:
        """Converts list of bits to bytes."""

        if isinstance(bits, BitArray):
            bits = bits.data

        result = bytearray([])
        for step in range(0, len(bits), 8):
            byte = bits[step : step + 8]

            # Pad with zeros if needed
            if len(byte) < 8:
                byte += [0] * (8 - len(byte))

            result.append(sum([2**i * v for i, v in enumerate(byte)]))

        return result

    def peek(self, length: int, offset: int = 0) -> list[int]:
        """Peek at next bits. Keep position unchanged."""

        return self.data[self.pos + offset : self.pos + offset + length]

    def read(self, length: int) -> list[int]:
        """Read next bits. Move position."""

        result = self.peek(length)
        self.pos += length

        return result

    def read_bytes(self, length: int) -> bytearray:
        """Read next bytes. Move position."""

        return self.bits_to_bytes(self.read(length * 8))

    def seek(self, location: int) -> Self:
        """Creates a copy of the array with a different position."""

        array_copy = copy.deepcopy(self)
        array_copy.pos = location

        return array_copy

    @classmethod
    def from_bits(cls, bits: list[int]) -> Self:
        """Creates a bitarray from list of bits."""

        return cls(cls.bits_to_bytes(bits))

    def write(self, bits: list[int] | Self) -> None:
        """Writes bits to the array."""

        self.data += bits if isinstance(bits, list) else bits.data
        self.pos = len(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __iadd__(self, other: Self) -> Self:
        if isinstance(other, BitArray):
            self.data += other.data
        elif isinstance(other, list):
            self.data += other
        return self
