from circular_dict import CircularDict
import numpy as np
import sys
import threading

def thread_function(_dict, start_index, num_operations):
    for i in range(num_operations):
        _dict[start_index + i] = start_index + i
        if (start_index + i) % 2 == 0:  # Arbitrarily delete some entries
            del _dict[start_index + i]

def concurrency_test():
    _dict = CircularDict(maxlen=50)
    threads = []
    num_threads = 500  # Number of concurrent threads
    operations_per_thread = 1000

    # Start threads
    for i in range(num_threads):
        thread = threading.Thread(target=thread_function, args=(_dict, i * operations_per_thread, operations_per_thread))
        threads.append(thread)

    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Verification
    assert len(_dict) <= _dict.maxlen, f"Dictionary exceeded its maximum length: {len(_dict)} > {_dict.maxlen}"


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

    # Check delete and pop
    del _dict[4]
    assert 4 not in _dict, "CircularDict should not contain the item 2"
    assert not _dict.is_full(), "CircularDict should not be full"
    assert len(_dict) == maxlen - 1, f"CircularDict should have {maxlen - 1} items. It has {len(_dict)} items"
    _dict[4] = 4
    assert _dict.is_full(), "CircularDict should be full"

def deletions_test(arrays_to_accept: int = 8, arrays_size: int = 10):
    # Calculate sizes for keys and values
    key_size = sys.getsizeof(1)
    value_size = sys.getsizeof(np.ones(arrays_size, dtype=np.int32))
    item_size = key_size + value_size

    # Initialize CircularDict with max size
    _dict = CircularDict(maxsize_bytes=(key_size + value_size) * arrays_to_accept)

    # Fill the dictionary with items (start on one because zero always occupies less space)
    for i in range(1, arrays_to_accept+1):
        array = np.array([i] * arrays_size, dtype=np.int32)
        _dict[i] = array

    assert _dict.is_full(), f"CircularDict should be full. It has a size of {_dict.current_size} bytes and the maximum size is {(_dict.maxsize_bytes)} bytes"

    # Check delete
    del _dict[arrays_to_accept]
    assert arrays_to_accept not in _dict, f"CircularDict should not contain the item {arrays_to_accept}"
    assert not _dict.is_full(), "CircularDict should not be full after deletion"
    assert len(_dict) == arrays_to_accept - 1, f"CircularDict should have {arrays_to_accept - 1} items. It has {len(_dict)} items"
    assert _dict.current_size == item_size * (
                arrays_to_accept - 1), "CircularDict current size should decrease after deletion"


    # Add the deleted item back to the dict
    array = np.array([arrays_to_accept] * arrays_size, dtype=np.int32)
    _dict[arrays_to_accept] = array
    assert _dict.is_full(), "CircularDict should be full after adding the deleted item back"
    assert _dict.current_size == item_size * arrays_to_accept, "CircularDict current size should be back to maximum after adding item back"

    # Check .pop() method
    popped_item = _dict.pop(arrays_to_accept)
    assert popped_item.tolist() == [arrays_to_accept] * arrays_size, "Popped item should be the same as the deleted one"
    assert arrays_to_accept not in _dict, f"CircularDict should not contain the item {arrays_to_accept} after pop"
    assert not _dict.is_full(), "CircularDict should not be full after pop"
    assert len(
        _dict) == arrays_to_accept - 1, f"CircularDict should have {arrays_to_accept - 1} items after pop. It has {len(_dict)} items"
    assert _dict.current_size == item_size * (
                arrays_to_accept - 1), "CircularDict current size should decrease after pop"

    # Check .popitem() method
    key, popped_item = _dict.popitem()
    assert popped_item.tolist() == [key] * arrays_size, "Popped item should be the same as the deleted one"
    assert key not in _dict, f"CircularDict should not contain the item {key} after popitem"
    assert not _dict.is_full(), "CircularDict should not be full after popitem"
    assert len(
        _dict) == arrays_to_accept - 2, f"CircularDict should have {arrays_to_accept - 2} items after popitem. It has {len(_dict)} items"
    assert _dict.current_size == item_size * (
                arrays_to_accept - 2), "CircularDict current size should decrease after popitem"

    # Check .clear() method
    _dict.clear()
    assert len(_dict) == 0, "CircularDict should be empty after clear"
    assert not _dict.is_full(), "CircularDict should not be full after clear"
    assert _dict.current_size == 0, "CircularDict current size should be zero after clear"


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

    assert _dict.is_full(), f"CircularDict should be full. It has a size of {_dict.current_size} bytes and the maximum size is {size_for_keys + size_for_values} bytes"


    # Try to add another array that exceeds the maximum size
    overflow_array = np.array([arrays_to_accept+1] * arrays_size, dtype=np.int32)
    _dict[arrays_to_accept+1] = overflow_array

    assert 1 not in _dict, f"The item with key 0 should have been removed from the CircularDict"
    assert 2 in _dict, f"The item with key 1 should still be in the CircularDict"

    assert len(_dict) == arrays_to_accept, f"The CircularDict should have {arrays_to_accept} items"
    assert _dict.current_size == (key_size + value_size) * arrays_to_accept, f"The CircularDict should have a size of {(key_size + value_size) * arrays_to_accept} bytes"

    assert tuple(_dict.keys()) == tuple(int(val[0]) for val in _dict.values()) == tuple(range(2, arrays_to_accept+2)),\
        f"CircularDict should contain the items {tuple(range(2, arrays_to_accept+2))}"


if __name__ == '__main__':

    maxlen_test()
    print("maxlen_test passed")
    maxsize_test()
    print("maxsize_test passed")
    deletions_test()
    print("deletions_test passed")

    concurrency_test()
    print("concurrency_test passed")