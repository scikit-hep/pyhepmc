from ._bindings import GenEvent


class _Iter:
    def __init__(self, parent):
        self.parent = parent
    def __iter__(self):
        return self
    def __next__(self):
        evt = self.parent.read()
        if evt is None:
            raise StopIteration
        return evt
_Iter.next = _Iter.__next__


def _enter(self):
    return self

def _exit(self, type, value, tb):
    self.close()
    return False

def _iter(self):
    return _Iter(self)

def _read(self):
    evt = GenEvent()
    ok = self.read_event(evt)
    return evt if ok and not self.failed() else None
