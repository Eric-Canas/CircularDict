"""
CircularDict: A dictionary that operates as a circular buffer, removing the oldest item when either maxlen or
              maxsize (in bytes) is exceeded. Useful for caching large items without using too much memory. This
              class is an implementation of the OrderedDict from the collections module and is designed to be
              highly efficient and scalable for use cases that require both, dictionary-like and
              circular-queue-like operations.

Author: Eric Canas
Date: 19-06-2023
Email: eric@ericcanas.com
Github: https://github.com/Eric-Canas
"""

import sys
from collections import OrderedDict
from typing import Any, Optional, Tuple
from threading import RLock

# To make sure it is compatible with PyPy environments (PyPy does not have sys.getsizeof for all types)
try:
    sys.getsizeof("Exist Check")
    getsizeof_available = True
except TypeError:
    sys.getsizeof = lambda x: 0
    getsizeof_available = False


class CircularDict(OrderedDict):
    """
    A dictionary that operates as a circular buffer, removing the oldest item when either maxlen or
    maxsize (in bytes) is exceeded.

    :param maxlen: Optional[int]. The maximum number of items in the dictionary.
    :param maxsize_bytes: Optional[int]. The maximum size of the dictionary in bytes.
    """

    def __init__(self, maxlen: Optional[int] = None, maxsize_bytes: Optional[int] = None, *args, **kwargs):
        """
        Initialize CircularDict.

        :param maxlen: Optional[int]. Maximum number of items in the dictionary.
        :param maxsize_bytes: Optional[int]. Maximum size of items in the dictionary in bytes.
        :param args: Positional arguments passed to OrderedDict.
        :param kwargs: Keyword arguments passed to OrderedDict.
        """
        assert maxlen is not None or maxsize_bytes is not None, "Either maxlen or maxsize must be set"
        if not getsizeof_available:
            assert maxsize_bytes is None, ("sys.getsizeof is not available for all types in this environment. "
                                           "That's common on, for example PyPy environments."
                                           "maxsize_bytes cannot be used. Set it to None.")

        self.maxlen = maxlen
        self.maxsize_bytes = maxsize_bytes
        self.current_size = 0

        self.lock = RLock()

        super().__init__(*args, **kwargs)

    def is_empty(self) -> bool:
        """
        Check if the dictionary is empty.

        :return: bool. True if empty, False otherwise.
        """
        empty = len(self) == 0
        if empty:
            assert self.current_size == 0, f"currentsize must be 0 when the dictionary is empty. currentsize={self.current_size}"
        return empty

    def is_full(self) -> bool:
        """
        Check if the dictionary is full. A full dictionary will remove the oldest item when a new item is added.

        :return: bool. True if full, False otherwise.
        """

        if self.maxsize_bytes is not None:
            assert self.current_size <= self.maxsize_bytes, f"currentsize must be less than or equal to maxsize. currentsize={self.current_size}, maxsize={self.maxsize_bytes}"

        if self.maxlen is not None:
            assert len(self) <= self.maxlen, f"len(self) must be less than or equal to self.maxlen. len(self)={len(self)}, self.maxlen={self.maxlen}"

        return (self.maxlen is not None and len(self) == self.maxlen) or (self.maxsize_bytes is not None and self.current_size == self.maxsize_bytes)

    def clear(self):
        """
        Remove all items from the dictionary.
        """
        with self.lock:
            super().clear()
            self.current_size = 0

    def __setitem__(self, key: Any, value: Any):
        """
        Set an item in the dictionary. If the key already exists, it will update the value.
        If the dictionary exceeds maxlen or maxsize, it will remove the oldest item until it no longer does.

        :param key: Any. Key to set or update. (It must be hashable)
        :param value: Any. Value to associate with the key.
        """
        item_size = sys.getsizeof(key) + sys.getsizeof(value)

        # If the element could not fit in the empty dictionary, raise an error
        if self.maxsize_bytes is not None:
            if item_size > self.maxsize_bytes:
                raise MemoryError(f"Item size {item_size} is larger than maxsize {self.maxsize_bytes}")

        with self.lock:
            # Delete the previous item if it exists to update the size accurately
            if key in self:
                del self[key]

            # Keep removing oldest items until there's enough space
            while self.maxsize_bytes is not None and self.current_size + item_size > self.maxsize_bytes:
                self.popitem(last=False)
            # Keep removing oldest items until there's
            while self.maxlen is not None and len(self) >= self.maxlen:
                assert len(self) == self.maxlen, f"len(self) must be equal to self.maxlen. len(self)={len(self)}, self.maxlen={self.maxlen}"
                self.popitem(last=False)

            OrderedDict.__setitem__(self, key, value)
            self.current_size += item_size  # add size of new item

    def __delitem__(self, key: Any):
        """
        Delete an item from the dictionary.

        :param key: Any. The key of the item to delete.
        """
        with self.lock:
            if key in self:
                value = self[key]
                self.current_size -= sys.getsizeof(key) + sys.getsizeof(value)
                OrderedDict.__delitem__(self, key)

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Remove specified key and return the corresponding value. Override of the default pop method,
        adapted to work with independently of the Python version (as Python 3.11 (and possibly later versions)
        does not call __delitem__ when popping).
        :param key: Any. The key of the item to pop.
        :param default: Any. The default value to return if the key is not found.
        :return: Any. The value associated with the key, or the default value if the key is not found.
        """
        with self.lock:
            # As pop doesn't work as expected with Python 3.11, this is a workaround
            if key not in self:
                if default is None:
                    raise KeyError(key)
                return default

            prev_size = self.current_size
            element = super().pop(key)

            element_size = sys.getsizeof(key) + sys.getsizeof(element)

            # If size did not change, because __delitem__ was not called (Python 3.11), then we must remove it manually
            if self.current_size == prev_size:
                self.current_size -= element_size
            else:
                # Otherwise, just assert to make sure everything is working as expected
                assert self.current_size == prev_size - element_size, f"currentsize must be equal to prev_size - element_size. currentsize={self.current_size}, prev_size={prev_size}, element_size={element_size}"

        return element

    def popitem(self, last: bool = True) -> Tuple[Any, Any]:
        """
        Remove and return a (key, value) pair from the dictionary.
        Pairs are returned in LIFO order if last is true or FIFO order if false.
        Override of the default popitem method, adapted to work independently of the
        Python version (as Python 3.11 (and possibly later versions) does not call __delitem__
        when popitem is used).

        :param last: bool. Return the last item (LIFO) if True, and the first item (FIFO) if False.
        :return: Tuple[Any, Any]. A key-value pair.
        """

        with self.lock:
            prev_size = self.current_size
            key, element = super().popitem(last=last)
            element_size = sys.getsizeof(key) + sys.getsizeof(element)

            # If size did not change, because __delitem__ was not called (Python 3.11), then we must remove it manually
            if self.current_size == prev_size:
                self.current_size -= element_size
            else:
                # Otherwise, just assert to make sure everything is working as expected
                assert self.current_size == prev_size - element_size, f"currentsize must be equal to prev_size - element_size. currentsize={self.current_size}, prev_size={prev_size}, element_size={element_size}"

        return key, element

