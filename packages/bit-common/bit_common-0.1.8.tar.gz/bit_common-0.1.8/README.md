# README.md

## bit-common

`bit-common` is a Python library that provides types and utilities for working with bits. It allows you to easily convert data to and from bits, making it a handy tool for low-level programming, data analysis, and more.

### Installation

You can install `bit-common` using pip or poetry.

#### Using pip

```bash
pip install bit-common
```

#### Using poetry

```bash
poetry add bit-common
```

### Usage

Here are some examples of how you can use `bit-common`.

#### Converting data to bits

```python
from bit import int8, UTF8StringWithPrefix

# Converting data to bits
data = int8(3)
bits = data.to_bits()
print(bits)  # Output: [1, 1, 0, 0, 0, 0, 0, 0]

# Converting bits to data
bits = [1, 1, 0, 0, 0, 0, 0, 0]
data = int8.from_bits(bits)
print(data)  # Output: 3

# Converting string to bits
string = UTF8StringWithPrefix("Hello")
bits = string.to_bits()
print(bits)  # Output: [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0]

# Converting bits to string
bits = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0]
string = UTF8StringWithPrefix.from_bits(bits)
print(string)  # Output: "Hello"
```


### License

`bit-common` is licensed under the MIT License.