"""
Visualization for GenEvent.
"""
from __future__ import annotations
from graphviz import Digraph
from ._prettify import db as _prettify
from . import Units as _Units
import numpy as np
from . import GenEvent
import os
from pathlib import PurePath
from typing import BinaryIO, TextIO, Union

# eps cannot handle utf-8 characters
SUPPORTED_BINARY_FORMATS = ("png", "gif", "svgz", "pdf")
SUPPORTED_TEXT_FORMATS = ("fig", "svg")
SUPPORTED_FORMATS = SUPPORTED_BINARY_FORMATS + SUPPORTED_TEXT_FORMATS


__all__ = ("to_dot", "savefig", "SUPPORTED_FORMATS")


def to_dot(
    evt: GenEvent,
    size: tuple[int, int] = None,
    color_hadron: str = "black",
    color_lepton_or_boson: str = "goldenrod",
    color_quark_or_gluon: str = "darkred",
    color_interal: str = "dodgerblue",
    color_invalid: str = "gainsboro",
    **kwargs,
) -> Digraph:
    """
    Convert GenEvent to Digraph.

    This converts the GenEvent into a graphviz Digraph in the DOT language,
    which in turn can be rendered in SVG format and displayed in Jupyter
    notebooks.

    Parameters
    ----------
    evt : GenEvent
        The event to convert.
    size : (int, int) or None, optional
        Maximum size of the graph in inches.
    color_hadron : str, optional
        Color (HTML color specification) for hadrons.
    color_lepton_or_boson: str, optional
        Color (HTML color specification) for leptons or bosons (gamma, W+/-, Z, H).
    color_quark_or_gluon: str, optional
        Color (HTML color specification) for quarks, diquarks, and gluons.
    color_internal: str, optional
        Color (HTML color specification) for generator-internal particles (e.g. Pomerons).
    color_invalid: str, optional
        Color (HTML color specification) for invalid particles (e.g. PID==0).
    """
    if evt.run_info:
        name = "\n".join(f"{t.name}-{t.version}" for t in evt.run_info.tools)
        name += "\n"
    else:
        name = ""
    name += f"event number = {evt.event_number}"

    d = Digraph(name=name)
    d.node_attr["shape"] = "point"
    d.graph_attr["rankdir"] = "LR"
    if size is None:
        size_s = "8,100"
    else:
        size_s = f"{size[0]},{size[1]}"
    d.graph_attr["size"] = size_s

    GeV = 1 if evt.momentum_unit == _Units.GEV else 1e3

    for v in evt.vertices:
        d.node(f"{v.id}", tooltip=f"{v.position} mm\nstatus = {v.status}")

    enmax = max(p.momentum.e / GeV for p in evt.particles)
    for p in evt.particles:
        en = p.momentum.e / GeV
        penwidth = str(max(0.5, 4 * en / enmax))

        unit = "GeV"
        if en > 1e2:
            en /= 1e3
            unit = "TeV"
        elif en < 1e-2:
            en *= 1e3
            unit = "MeV"

        style = "solid"

        pname = _prettify.get(p.pid, None)
        if pname is None:
            if p.pid == 0:
                pname = "Invalid(0)"
                color = color_invalid
                penwidth = "7"
            else:
                pname = f"Internal({p.pid})"
                color = color_interal
                penwidth = "7"

        tooltip = f"{pname} [PDGID: {int(p.pid)}]"
        tooltip += f"\n{p.momentum} GeV"
        tooltip += f"\nm = {p.generated_mass:.4g} GeV"
        tooltip += f"\nstatus = {p.status}"

        try:
            from particle import PDGID, Particle, ParticleNotFound, InvalidParticle

            pdgid = PDGID(p.pid)

            if pdgid.is_hadron or pdgid.is_nucleus:
                if pdgid.is_nucleus:
                    tooltip += f"\nA,Z = {pdgid.A},{pdgid.Z}"
                color = color_hadron
            elif pdgid == 21 or pdgid.is_quark or pdgid.is_diquark:
                color = color_quark_or_gluon
            elif pdgid.is_lepton or pdgid.is_gauge_boson_or_higgs:
                color = color_lepton_or_boson
            else:
                color = color_interal

            try:
                pdb = Particle.from_pdgid(p.pid)
                tooltip += f"\nquarks = {pdb.quarks}"
                tooltip += f"\nQ = {pdb.charge:.3g}"
                if pdb.ctau and np.isfinite(pdb.ctau):
                    tooltip += f"\ncτ = {pdb.ctau:.3g} mm"
                if pdb.charge == 0:
                    style = "dashed"
            except (ParticleNotFound, InvalidParticle):
                pass
        except ModuleNotFoundError:  # pragma: no cover
            color = "black"  # pragma: no cover

        label = f"{pname} {en:.2g} {unit}"

        # do not connect initial particles to root vertex
        if p.production_vertex and p.production_vertex.id != 0:
            vin = f"{p.production_vertex.id}"
        else:
            vin = f"in_{p.id}"
            d.node(vin, style="invis")

        if p.end_vertex:
            vout = f"{p.end_vertex.id}"
        else:
            vout = f"out_{p.id}"
            d.node(vout, style="invis")

        if not p.production_vertex or p.production_vertex.id == 0 and p.end_vertex:
            # initial particle which is not also final state is beam particle
            edir = "forward"
        elif p.status == 1:  # final state
            edir = "forward"
        else:  # intermediate
            edir = "none"

        d.edge(
            vin,
            vout,
            dir=edir,
            label=label,
            color=color,
            style=style,
            tooltip=tooltip,
            labeltooltip=tooltip,
            penwidth=penwidth,
        )

    return d


def savefig(event: Union[GenEvent, Digraph], fname: Union[str,os.PathLike,TextIO,BinaryIO], *, format: str = None, **kwargs):
    """
    Save event as an image.

    The SVG format is recommended, because it contains tooltips with extra information.
    
    Supported formats: {SUPPORTED_FORMATS}.

    Parameters
    ----------
    event : GenEvent or Digraph
        The event to be saved.
    fname : path-like or file-like
        Path or file-like handle to which the image is written.
    format : str, optional
        Output format.
    **kwargs :
        Other arguments are forwarded to pyhepmc.view.to_dot.
    """
    if isinstance(fname, (str, os.PathLike)):
        p = PurePath(fname)
        if format is None:
            format = p.suffix[1:]
        if format in SUPPORTED_BINARY_FORMATS:
            with open(p, "wb") as fo:
                savefig(event, fo, format=format, **kwargs)
        elif format in SUPPORTED_TEXT_FORMATS:
            with open(p, "wb") as fo:
                savefig(event, fo, format=format, **kwargs)
        # unknown format raises exception in nested call
        with open(os.devnull, "wb") as fo:
            savefig(event, fo, format=format, **kwargs)
        return

    # if we arrive here, fname is a file-like object or None

    if format is None:
        raise ValueError("When using file-like object, keyword 'format' must be set")

    if format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Format {format!r} not supported (supported formats: {', '.join(SUPPORTED_FORMATS)})")

    if isinstance(event, GenEvent):
        g = to_dot(event, **kwargs)
    else:
        if kwargs:
            import warnings

            warnings.warn(f"Extra kwargs are ignored when passing DiGraph",
                RuntimeWarning
            )
        g = event

    encoding = 'utf-8' if isinstance(fname, TextIO) else None
    s = g.pipe(format=format, encoding=encoding)

    fname.write(s)

savefig.__doc__ = savefig.__doc__.format(SUPPORTED_FORMATS=", ".join(SUPPORTED_FORMATS))