# CircularDict
<img alt="CircularDict" title="CircularDict" src="https://raw.githubusercontent.com/Eric-Canas/CircularDict/main/resources/logo.png" width="20%" align="left"> **CircularDict** is a Python `dict` that acts as a **Circular Buffer**. This dictionary maintains a **controlled size**, limited either by a specified **number of items** (_maxlen_) or **total size in bytes** (_maxsize_bytes_). Upon reaching the defined limit, **CircularDict** automatically removes the oldest entries, maintaining **memory usage** under control.

Built upon Python's `OrderedDict`, **CircularDict** inherits all **standard dictionary usage** and operations, augmented by the capability of **memory management**. It's particularly useful in scenarios such as **caching**, where limiting **memory consumption** is crucial. The class combines _dictionary_ and _circular-queue_ behaviors, providing an efficient and scalable solution for various use cases.

## Installation

To install **CircularDict** simply run:

```bash
pip install circular-dict
```

## Usage

Working with **CircularDict** is as simple as using a standard Python `dict`, with additional parameters `maxlen` or `maxsize_bytes` on the initialization to control the buffer size. You can use one of them or both.
```python
from circular_dict import CircularDict
# Initialize a CircularDict with a maximum length of 3 items and a storage limit of 4Mb
my_dict = CircularDict(maxlen=3, maxsize_bytes=4*1024*1024)
```

### Example with `maxlen`
You can use `maxlen` to define the maximum amount of items that the dictionary can store. It is useful for defining fixed size buffers.

```python
from circular_dict import CircularDict

# Initialize a CircularDict with a maximum length of 3
my_buffer = CircularDict(maxlen=3)

# Fill it with 3 items
my_buffer['item1'] = 'value1'
my_buffer['item2'] = 'value2'
my_buffer['item3'] = 'value3'

print(f"When filling it: {circ_dict}")

# Add another item
my_buffer['item4'] = 'value4'

print(f"After adding an element beyond maxlen: {circ_dict}")
```

Output:
```bash
When filling it: {'item1': 'value1', 'item2': 'value2', 'item3': 'value3'}
After adding an element beyond maxlen: {'item2': 'value2', 'item3': 'value3', 'item4': 'value4'}
```

### Example with `maxsize_bytes`
You can use `maxsize_bytes` to define the maximum amount of memory that the `dict` can store. It is particularly beneficial when defining **caches**, to prevent **memory overflows**.

```python
from circular_dict import CircularDict
import numpy as np
import sys

# Initialize a CircularDict with a maximum length of 100KB
my_buffer = CircularDict(maxsize_bytes=100*1024)

# Add two arrays of ~40Kb (10*1024*4 bytes (int32) + 5 bytes (chars) + 100 bytes (numpy structure) + 50 bytes (str structure))
my_buffer['item1'] = np.zeros((10, 1024), dtype=np.int32)
my_buffer['item2'] = np.ones((10, 1024), dtype=np.int32)

print(f"{len(my_buffer)} Elements {tuple(my_buffer.keys())}. Dict size: {my_buffer.current_size/1024} Kb")

# Add a new element of ~32Kb will delete oldest elements ('item1') until fitting in the `dict`.
my_buffer['item3'] = np.ones((8, 1024), dtype=np.int32)

print(f"{len(my_buffer)} Elements {tuple(my_buffer.keys())}. Dict size: {my_buffer.current_size/1024} Kb")

# Create an element of ~160Kb (bigger than the defined maximum storage) to trigger a MemoryError
too_big_array = np.ones((40, 1024), dtype=np.int32)
try:
  # Try to add it to the dict
  my_buffer['item4'] = too_big_array
except MemoryError:
  print(f"Cannot add an element with {sys.getsizeof(too_big_array)/1024}Kb in a dict with"\
        f"maxsize_bytes of {my_buffer.maxsize_bytes/1024} Kb. Current elements {tuple(my_buffer.keys())}")
```

Output

```bash
2 Elements ('item1', 'item2'). Dict size: 80.35 Kb
2 Elements ('item2', 'item3'). Dict size: 72.35 Kb
Cannot add an element with 160.12Kb in a dict with maxsize_bytes of 100.0 Kb. Current elements ('item2', 'item3')
```

Please remember that the `maxsize_bytes` parameter considers the **total** memory footprint, including the sizes of _keys_ and _values_. If you try to add an item that exceeds the `maxsize_bytes`, a `MemoryError` will be raised.
