from typing import Any, Tuple, Generator, Dict


def clear(self: Any) -> None:
    for key in list(self):
        del self[key]


def items(
    self: Any,
) -> Generator[Tuple[str, Any], None, None]:
    for name in self:
        yield name, self[name]


def eq(self: Any, other: Dict[str, Any]) -> bool:
    if len(self) != len(other):
        return False
    for k, v in self.items():
        if k not in other:
            return False
        if v != other[k]:
            return False
    return True


def repr(self: Any) -> str:
    s = f"<{self.__class__.__name__}>{{"
    first = True
    for k, v in self.items():
        if not first:
            s += ", "
        first = False
        s += f"{k!r}: {v!r}"
    s += "}"
    return s


def install() -> None:
    from pyhepmc._core import AttributesView, RunInfoAttributesView

    AttributesView.clear = clear
    AttributesView.items = items
    AttributesView.__eq__ = eq
    AttributesView.__repr__ = repr

    RunInfoAttributesView.clear = clear
    RunInfoAttributesView.items = items
    RunInfoAttributesView.__eq__ = eq
    RunInfoAttributesView.__repr__ = repr
