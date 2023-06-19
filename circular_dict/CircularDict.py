"""
CircularDict: A dictionary that operates as a circular buffer, removing the oldest item when maxlen is exceeded.
               Useful for caching large items without using too much memory. This class is an implementation of
               the OrderedDict from the collections module and is designed to be highly efficient and scalable
               for use cases that require both, dictionary-like and circular-queue-like operations.

Author: Eric Canas
Date: 19-06-2023
Email: eric@ericcanas.com
Github: https://github.com/Eric-Canas
"""

from collections import OrderedDict
from typing import Any

class CircularDict(OrderedDict):
    """
    A dictionary that operates as a circular buffer, removing the oldest item when maxlen is exceeded.
    Useful for caching large items without using too much memory.

    :param maxlen: The maximum length of the dictionary.
    """
    def __init__(self, maxlen: int):
        """
        Initialize CircularDict.

        :param maxlen: int. Maximum number of items in the dictionary.
        """
        assert maxlen > 0, f"maxlen must be greater than 0, got {maxlen}"
        self.maxlen = maxlen
        super().__init__()

    def __setitem__(self, key: Any, value: Any):
        """
        Set an item in the dictionary. If the key already exists, it will update the value.
        If the dictionary is full, it will remove the oldest item.

        :param key: Any. Key to set or update. (It must be hashable)
        :param value: Any. Value to associate with the key.
        """
        if key in self:
            del self[key]
        elif len(self) >= self.maxlen:
            self.popitem(last=False)  # remove the oldest item

        OrderedDict.__setitem__(self, key, value)

    def is_empty(self) -> bool:
        """
        Check if the dictionary is empty.

        :return: bool. True if empty, False otherwise.
        """
        return len(self) == 0

    def is_full(self) -> bool:
        """
        Check if the dictionary is full. A full dictionary will remove the oldest item when a new item is added.

        :return: bool. True if full, False otherwise.
        """
        assert len(self) <= self.maxlen, f"len(self) must be less than or equal to self.maxlen. len(self)={len(self)}, self.maxlen={self.maxlen}"
        return len(self) == self.maxlen