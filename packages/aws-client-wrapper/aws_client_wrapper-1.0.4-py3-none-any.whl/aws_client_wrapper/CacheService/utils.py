"""Cache utils"""
from builtins import object
from collections.abc import MutableMapping


class ReadOnlyDict(MutableMapping):
    def __init__(self, d):
        self.d = d

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        raise NotImplementedError("Read-only dictionary")

    def __delitem__(self, key):
        raise NotImplementedError("Read-only dictionary")

    def __iter__(self):
        return iter(self.d)

    def __len__(self):
        return len(self.d)

    def __contains__(self, key):
        return key in self.d

    def __json__(self):
        return dict(self.d)

    def __repr__(self):
        return repr(self.d)


class ReadOnlySet(object):
    def __init__(self, s):
        self.s = set(s)

    def __getitem__(self, item):
        raise TypeError("'ReadOnlySet' object does not support indexing")

    def __setitem__(self, item, value):
        raise NotImplementedError("Read-only set")

    def __delitem__(self, item):
        raise NotImplementedError("Read-only set")

    def __iter__(self):
        return iter(self.s)

    def __len__(self):
        return len(self.s)

    def __contains__(self, item):
        return item in self.s

    def __json__(self):
        return list(self.s)

    def __repr__(self):
        return repr(self.s)


class ReadOnlyList(object):
    def __init__(self, lst):
        self.lst = list(lst)

    def __getitem__(self, index):
        return self.lst[index]

    def __iter__(self):
        return iter(self.lst)

    def __len__(self):
        return len(self.lst)

    def __contains__(self, item):
        return item in self.lst

    def __setitem__(self, index, value):
        raise NotImplementedError("Read-only list")

    def __delitem__(self, index):
        raise NotImplementedError("Read-only list")

    def __json__(self):
        return self.lst

    def __repr__(self):
        return repr(self.lst)
