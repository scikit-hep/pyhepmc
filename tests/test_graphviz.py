from __future__ import annotations

from collections import Counter

import pytest

import pyhepmc
from pyhepmc import view
from pyhepmc._graphviz import Block, Digraph


def edge_lines(graph):
    return [line for line in str(graph).splitlines() if " -> " in line]


def test_to_dot_parallel_particles():
    event = pyhepmc.GenEvent()
    decay, hadronize = pyhepmc.GenVertex(), pyhepmc.GenVertex()
    W = pyhepmc.GenParticle((0, 0, 0, 80), 24, 2)
    q = pyhepmc.GenParticle((0, 0, 40, 40), 2, 2)
    antiquark = pyhepmc.GenParticle((0, 0, -40, 40), -1, 2)
    cluster = pyhepmc.GenParticle((0, 0, 0, 80), 91, 1)
    decay.add_particle_in(W)
    decay.add_particle_out(q)
    decay.add_particle_out(antiquark)
    hadronize.add_particle_in(q)
    hadronize.add_particle_in(antiquark)
    hadronize.add_particle_out(cluster)
    event.add_vertex(decay)
    event.add_vertex(hadronize)
    expected = Counter(p.pid for p in event.particles)

    graph = view.to_dot(event)

    assert [p.pid for p in W.children] == [2, -1]
    assert len(graph.edges) == len(event.particles) == 4
    observed = Counter(
        int(block["tooltip"].splitlines()[0].split(" = ")[1])
        for block in graph.edges.values()
    )
    assert observed == expected
    parallel = f"{decay.id} -> {hadronize.id}"
    assert sum(line.startswith(parallel + " [") for line in edge_lines(graph)) == 2
    assert set(graph.nodes) == {str(decay.id), str(hadronize.id), "in_1", "out_4"}


@pytest.mark.parametrize("end", ["b", "a"])
def test_parallel_edges_with_identical_attributes(end):
    graph = Digraph()
    graph.edge("a", end, label="same", color="red", style="dashed")
    first = graph.edges[f"a -> {end}"]
    graph.edge("a", end, label="same", color="red", style="dashed")
    graph.edge("a", end, label="same", color="red", style="dashed")

    assert isinstance(graph.edges, dict)
    assert len(graph.edges) == 3
    assert graph.edges[f"a -> {end}"] is first
    assert list(graph.edges.values()) == [first, first, first]
    assert (
        edge_lines(graph)
        == [f'a -> {end} [dir=none, label="same", color=red, style=dashed]'] * 3
    )


def test_parallel_edge_insertion_order():
    graph = Digraph()
    graph.edge("a", "b", label="first")
    graph.edge("c", "d", label="middle")
    graph.edge("a", "b", label="last")

    assert [block["label"] for block in graph.edges.values()] == [
        "first",
        "middle",
        "last",
    ]
    assert edge_lines(graph) == [
        'a -> b [dir=none, label="first"]',
        'c -> d [dir=none, label="middle"]',
        'a -> b [dir=none, label="last"]',
    ]


def test_legacy_dictionary_constructor_and_parallel_repr():
    original = Block(label="original", color="blue")
    edges = {"a -> b": original}
    graph = Digraph(name="event", edges=edges)
    graph.edge("a", "b", label="new", color="red")

    assert graph.edges is edges
    assert graph.edges["a -> b"] is original
    assert list(graph.edges.values()) == [
        original,
        Block(dir="none", label="new", color="red"),
    ]
    graph2 = eval(repr(graph), {"Digraph": Digraph, "Block": Block})
    assert graph2 == graph
    assert str(graph2) == str(graph)


def test_constructor_duplicate_key_collision():
    first = Block(label="first")
    existing = Block(label="existing")
    graph = Digraph(edges={"a -> b": first, ("a -> b", 2): existing})
    graph.edge("a", "b", label="new")

    assert len(graph.edges) == 3
    assert graph.edges["a -> b"] is first
    assert graph.edges[("a -> b", 2)] is existing
    assert edge_lines(graph) == [
        'a -> b [label="first"]',
        'a -> b [label="existing"]',
        'a -> b [dir=none, label="new"]',
    ]


def test_duplicate_key_collision_after_deletion():
    graph = Digraph()
    graph.edge("a", "b", label="first")
    graph.edge("c", "d", label="deleted")
    graph.edge("a", "b", label="existing")
    del graph.edges["c -> d"]
    graph.edge("a", "b", label="new")

    assert len(graph.edges) == 3
    assert [block["label"] for block in graph.edges.values()] == [
        "first",
        "existing",
        "new",
    ]
    assert all(line.startswith("a -> b [") for line in edge_lines(graph))


def test_nonparallel_dot_unchanged():
    graph = Digraph(name="event")
    graph.graph_attr["rankdir"] = "LR"
    graph.node("a", tooltip="origin")
    graph.node("b")
    graph.edge(
        "a",
        "b",
        dir="forward",
        label="p",
        color="red",
        style="dashed",
        penwidth="2",
        tooltip="custom",
        labeltooltip="custom label",
    )

    assert str(graph) == (
        'digraph "event" {\n'
        "graph [rankdir=LR]\n"
        "node []\n"
        'a [tooltip="origin"]\n'
        "b []\n"
        'a -> b [dir=forward, label="p", color=red, style=dashed, penwidth=2, '
        'tooltip="custom", labeltooltip="custom label"]\n'
        "}"
    )
