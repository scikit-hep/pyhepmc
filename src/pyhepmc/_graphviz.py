from __future__ import annotations

import dataclasses
import subprocess as subp
import threading

from packaging.version import Version

try:
    import pygraphviz as pygraphviz  # noqa: PLC0414 - explicit re-export for view
except ImportError:
    pygraphviz = None

# Version 2 renders through the library instead of spawning a layout process.
if pygraphviz is not None and Version(pygraphviz.__version__) < Version("2"):
    pygraphviz = None

_render_lock = threading.Lock()
# Keep plugin-specific formats on the executable backend. In particular,
# PyGraphviz 2.0.4's bundled build lacks several Windows/raster plugins, and
# its FIG renderer retains state between calls.
_library_formats = {
    "svg",
    "svg_inline",
    "svgz",
    "png",
    "pdf",
    "ps",
    "ps2",
    "dot",
    "gv",
    "canon",
    "plain",
    "plain-ext",
    "json",
    "dot_json",
    "xdot",
    "xdot1.2",
    "xdot1.4",
    "xdot_json",
    "cmap",
    "cmapx",
    "cmapx_np",
    "jpg",
    "jpeg",
    "jpe",
    "gif",
    "wbmp",
    "pic",
    "vrml",
}


class Value(str):
    pass


class Quoted(str):
    def __str__(self) -> str:
        s = super().__str__()
        return f'"{s}"'


class Block(dict[str, Quoted | Value]):
    def __init__(self, **kwargs: str):
        super().__init__()
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def __setitem__(self, key: str, value: str) -> None:
        if not value:
            return
        value_type: type[Value | Quoted] = Value
        if key in ("size", "label", "tooltip", "labeltooltip"):
            value_type = Quoted
        super().__setitem__(key, value_type(value))

    def __str__(self) -> str:
        s = []
        for k, v in self.items():
            s.append(f"{k}={v}")
        return f"[{', '.join(s)}]"

    def __repr__(self) -> str:
        s = []
        for k, v in self.items():
            s.append(f"{k}={v!r}")
        return f"Block({', '.join(s)})"


@dataclasses.dataclass
class Digraph:
    name: Quoted
    graph_attr: Block
    node_attr: Block
    nodes: dict[str, Block]
    edges: dict[str, Block]

    def __init__(
        self,
        *,
        name: str = "",
        graph_attr: Block | None = None,
        node_attr: Block | None = None,
        nodes: dict[str, Block] | None = None,
        edges: dict[str, Block] | None = None,
    ):
        self.name = Quoted(name)
        self.graph_attr = graph_attr or Block()
        self.node_attr = node_attr or Block()
        self.nodes = nodes or {}
        self.edges = edges or {}

    def edge(
        self,
        vin: str,
        vout: str,
        *,
        dir: str = "none",
        label: str = "",
        color: str = "",
        style: str = "",
        penwidth: str = "",
        tooltip: str = "",
        labeltooltip: str = "",
    ) -> None:
        self.edges[f"{vin} -> {vout}"] = Block(
            dir=dir,
            label=label,
            color=color,
            style=style,
            penwidth=penwidth,
            tooltip=tooltip,
            labeltooltip=labeltooltip,
        )

    def node(self, id: str, *, style: str = "", tooltip: str = "") -> None:
        self.nodes[f"{id}"] = Block(tooltip=tooltip, style=style)

    def __str__(self) -> str:
        s = [
            f"graph {self.graph_attr}",
            f"node {self.node_attr}",
        ]
        for k, v in self.nodes.items():
            s.append(f"{k} {v}")
        for k, v in self.edges.items():
            s.append(f"{k} {v}")
        nl = "\n"
        return f"digraph {self.name} {{\n{nl.join(s)}\n}}"

    def pipe(self, *, format: str, encoding: str | None = None) -> str | bytes:
        input = str(self)
        if pygraphviz is not None and format in _library_formats:
            # Graphviz uses global native state. Serialize calls and release each
            # graph while retaining the process's initialized font machinery.
            with _render_lock:
                graph = pygraphviz.AGraph(string=input)
                try:
                    output = graph.draw(format=format, prog="dot")
                except (ValueError, TypeError):
                    # The installed dot may provide plugins absent from the
                    # Graphviz library bundled with PyGraphviz. Version 2.0.4
                    # raises TypeError when gvRenderData returns an error code.
                    pass
                else:
                    assert isinstance(output, bytes)
                    return output.decode(encoding) if encoding else output
                finally:
                    graph.close()
        try:
            r = subp.run(
                ["dot", f"-T{format}"],
                capture_output=True,
                check=False,
                input=input.encode("utf-8"),
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                "command `dot` cannot be found, please install graphviz"
            )
        if r.returncode != 0:
            msg = r.stderr.decode("utf-8")
            match = "Error: <stdin>: "
            idx = msg.find(match)
            if idx >= 0:
                idx += len(match)
                msg = msg[idx:]
            msg += "\n" + input
            raise ValueError(msg)
        if encoding:
            return r.stdout.decode(encoding)
        return r.stdout

    def _repr_svg_(self) -> str:
        try:
            s = self.pipe(format="svg", encoding="utf-8")
            assert isinstance(s, str)
        except FileNotFoundError as e:
            return f"SVG view not available: {e.args[0]}"
        return s

    def _repr_png_(self) -> bytes:
        b = self.pipe(format="png")
        assert isinstance(b, bytes)
        return b

    def _repr_html_(self) -> str:
        return self._repr_svg_()
