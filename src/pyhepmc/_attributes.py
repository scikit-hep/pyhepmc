from ._core import AttributesView, RunInfoAttributesView
import typing as _tp


def _clear(self: _tp.Any) -> None:
    for key in list(self):
        del self[key]


def _items(
    self: _tp.Any,
) -> _tp.Generator[_tp.Tuple[str, _tp.Any], None, None]:
    for name in self:
        yield name, self[name]


def _eq(self: _tp.Any, other: _tp.Dict[str, _tp.Any]) -> bool:
    if len(self) != len(other):
        return False
    for k, v in self.items():
        if k not in other:
            return False
        if v != other[k]:
            return False
    return True


def _repr(self: _tp.Any) -> str:
    s = f"<{self.__class__.__name__}>{{"
    first = True
    for k, v in self.items():
        if not first:
            s += ", "
        first = False
        s += f"{k!r}: {v!r}"
    s += "}"
    return s


AttributesView.clear = _clear
AttributesView.items = _items
AttributesView.__eq__ = _eq
AttributesView.__repr__ = _repr

RunInfoAttributesView.clear = _clear
RunInfoAttributesView.items = _items
RunInfoAttributesView.__eq__ = _eq
RunInfoAttributesView.__repr__ = _repr
