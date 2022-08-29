from pyhepmc._deprecated import deprecated
import pytest
import numpy as np


class Foo:
    @deprecated("use baz")
    def bar(self):
        return 0


def test_deprecated():
    foo = Foo()

    with pytest.raises(ValueError, match="reason.*required"):

        @deprecated
        def bad(self):
            return 0

    with pytest.warns(np.VisibleDeprecationWarning, match="bar is deprecated: use baz"):
        foo.bar()
