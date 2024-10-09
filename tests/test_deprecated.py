from pyhepmc._deprecated import deprecated
import pytest


class Foo:
    @deprecated("use baz")
    def bar(self):
        return 0

    @deprecated("use baz", removal="1000.0.0")
    def foo(self):
        return 0


def test_deprecated():
    foo = Foo()

    with pytest.raises(AssertionError):

        @deprecated
        def bad(self):
            return 0

    with pytest.warns(DeprecationWarning, match="bar is deprecated: use baz"):
        foo.bar()

    with pytest.warns(
        DeprecationWarning,
        match="foo is deprecated and will be removed in version 1000.0.0: use baz",
    ):
        foo.foo()
