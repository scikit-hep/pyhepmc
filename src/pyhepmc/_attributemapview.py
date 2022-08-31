from ._core import AttributeMapView
import typing as _tp


def _clear(self: AttributeMapView) -> None:
    for key in list(self):
        del self[key]


def _items(
    self: AttributeMapView,
) -> _tp.Generator[_tp.Tuple[str, _tp.Any], None, None]:
    for name in self:
        yield name, self[name]


def _eq(self: AttributeMapView, other: _tp.Dict[str, _tp.Any]) -> bool:
    if len(self) != len(other):
        return False
    for k, v in self.items():
        if k not in other:
            return False
        if v != other[k]:
            return False
    return True


def _repr(self: AttributeMapView) -> str:
    s = "<AttributeMapView>{"
    first = True
    for k, v in self.items():
        if not first:
            s += ", "
        first = False
        s += f"{k!r}: {v!r}"
    s += "}"
    return s


AttributeMapView.clear = _clear
AttributeMapView.items = _items
AttributeMapView.__eq__ = _eq
AttributeMapView.__repr__ = _repr
