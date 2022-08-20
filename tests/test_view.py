import pytest
from test_basic import evt  # noqa

view = pytest.importorskip("pyhepmc.view")  # depends on graphviz


def test_dot(tmpdir, evt):  # noqa
    import os

    os.chdir(str(tmpdir))
    d = view.to_dot(evt)
    assert str(d) == (
        """digraph "event 1" {
    node [shape=point]
    -1
    -2
    -3
    -4
    in_0 [style=invis]
    in_0 -> -1 [label="p\n7 GeV"]
    in_1 [style=invis]
    in_1 -> -2 [label="p\n7 GeV"]
    -1 -> -3 [label="d\n0.032 GeV"]
    -2 -> -3 [label="u~\n0.058 GeV"]
    -3 -> -4 [label="W-\n0.086 GeV"]
    out_0 [style=invis]
    -3 -> out_0 [label="gamma\n0.0042 GeV"]
    out_1 [style=invis]
    -4 -> out_1 [label="d\n0.03 GeV"]
    out_2 [style=invis]
    -4 -> out_2 [label="u~\n0.056 GeV"]
}
""".replace(
            "    ", "\t"
        )
    )
    # d.render(view=True)
