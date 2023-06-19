from circular_dict import CircularDict
import numpy as np
import sys

def maxlen_test(maxlen: int = 5, items_to_overflow: int = 3):
    _dict = CircularDict(maxlen=maxlen)
    assert _dict.is_empty(), "CircularDict should be empty"
    assert not _dict.is_full(), "CircularDict should not be full"

    # Fill the dictionary with maxlen items
    for i in range(maxlen):
        _dict[i] = i
        assert not _dict.is_empty(), "CircularDict should not be empty"

    assert _dict.is_full(), f"CircularDict should be full. It has {len(_dict)} items and the maximum length is {maxlen}"

    assert tuple(_dict.keys()) == tuple(_dict.values()) == tuple(range(maxlen)), f"CircularDict should contain the items {tuple(range(maxlen))}"

    # Add items_to_overflow more items, the oldest items should be removed
    for i in range(maxlen, maxlen + items_to_overflow):
        _dict[i] = i
        assert _dict.is_full(), "CircularDict should be full"

    assert tuple(_dict.keys()) == tuple(_dict.values()) == tuple(range(maxlen-(maxlen-items_to_overflow), maxlen+items_to_overflow)),\
        f"CircularDict should contain the items {tuple(range(maxlen-(maxlen-items_to_overflow), maxlen+items_to_overflow))}"

    assert not any(i in _dict for i in range(0, maxlen-items_to_overflow)), f"CircularDict should not contain the items {tuple(range(0, maxlen-items_to_overflow))}"


def maxsize_test(arrays_to_accept: int = 8, arrays_size: int = 10):
    # Calculate sizes for keys and values
    key_size = sys.getsizeof(1)
    value_size = sys.getsizeof(np.ones(arrays_size, dtype=np.int32))

    # Initialize CircularDict with max size
    _dict = CircularDict(maxsize_bytes=(key_size + value_size) * arrays_to_accept)
    assert _dict.is_empty(), "CircularDict should be empty"
    assert not _dict.is_full(), "CircularDict should not be full"

    # Fill the dictionary with items (start on one because zero always occupies less space)
    for i in range(1, arrays_to_accept+1):
        array = np.array([i] * arrays_size, dtype=np.int32)
        assert sys.getsizeof(array) == value_size, f"Each array should have a size of {value_size} bytes"
        assert sys.getsizeof(i) == key_size, f"Each key should have a size of {key_size} bytes"
        _dict[i] = array
        assert not _dict.is_empty(), "CircularDict should not be empty"

    assert _dict.is_full(), f"CircularDict should be full. It has a size of {_dict.currentsize} bytes and the maximum size is {size_for_keys + size_for_values} bytes"


    # Try to add another array that exceeds the maximum size
    overflow_array = np.array([arrays_to_accept+1] * arrays_size, dtype=np.int32)
    _dict[arrays_to_accept+1] = overflow_array

    assert 1 not in _dict, f"The item with key 0 should have been removed from the CircularDict"
    assert 2 in _dict, f"The item with key 1 should still be in the CircularDict"

    assert len(_dict) == arrays_to_accept, f"The CircularDict should have {arrays_to_accept} items"
    assert _dict.currentsize == (key_size + value_size) * arrays_to_accept, f"The CircularDict should have a size of {(key_size + value_size) * arrays_to_accept} bytes"

    assert tuple(_dict.keys()) == tuple(int(val[0]) for val in _dict.values()) == tuple(range(2, arrays_to_accept+2)),\
        f"CircularDict should contain the items {tuple(range(2, arrays_to_accept+2))}"


if __name__ == '__main__':

    maxlen_test()
    print("maxlen_test passed")
    maxsize_test()
    print("maxsize_test passed")