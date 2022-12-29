import dataclasses
from typing import Union, Dict, Type
import subprocess as subp


class Value(str):
    pass


class Quoted(str):
    def __str__(self) -> str:
        s = super().__str__()
        return f'"{s}"'


class Block(Dict[str, Union[Quoted, Value]]):
    def __init__(self, **kwargs: str):
        super().__init__()
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def __setitem__(self, key: str, value: str) -> None:
        if not value:
            return
        type: Union[Type[Value], Type[Quoted]] = Value
        if key in ("size", "label", "tooltip", "labeltooltip"):
            type = Quoted
        super().__setitem__(key, type(value))

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
    nodes: Dict[str, Block]
    edges: Dict[str, Block]

    def __init__(
        self,
        *,
        name: str = "",
        graph_attr: Block = None,
        node_attr: Block = None,
        nodes: Dict[str, Block] = None,
        edges: Dict[str, Block] = None,
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

    def pipe(self, *, format: str, encoding: str = None) -> Union[str, bytes]:
        input = str(self)
        try:
            r = subp.run(
                ["dot", f"-T{format}"], capture_output=True, input=input.encode("utf-8")
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
        s = self.pipe(format="svg", encoding="utf-8")
        assert isinstance(s, str)
        return s

    def _repr_png_(self) -> bytes:
        b = self.pipe(format="png")
        assert isinstance(b, bytes)
        return b

    def _repr_html_(self) -> str:
        return self._repr_svg_()
