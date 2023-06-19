from circular_dict import CircularDict

if __name__ == '__main__':
    maxlen = 5
    items_to_overflow = 3

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

    print("Everything is working as expected")