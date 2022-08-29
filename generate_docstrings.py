from pathlib import Path  # noqa
import subprocess as subp
import xml.etree.ElementTree as ET
from collections import defaultdict

cdir = Path(__file__).parent

if not (cdir / "docs" / "xml").exists():
    subp.check_call(["doxygen", "docs/Doxyfile"])

with open(cdir / "src" / "pyhepmc" / "_autodoc.py", "w") as f:
    f.write("autodoc = {}\n")

IGNORED = {
    "HEPEVT_Pointers",
    "HEPEVT_Templated",
    "HEPEVT_Wrapper",
    "HEPEVT_Wrapper_Runtime",
    "HEPEVT_Wrapper_Template",
    "HEPEVT_Wrapper_Runtime_Static",
    "Print.line",
    "GenParticlePtr_greater",
    "pair_GenVertexPtr_int_greater",
    "ReaderPlugin",
    "WriterPlugin",
    "Reader",
    "Writer",
    "FourVector.set",
    "FourVector.set_component",
    "FourVector.get_component",
    "FourVector.ZERO_VECTOR",
}


def object_visitor(objects, prefix, obj):
    if not hasattr(obj, "__dict__"):
        return

    for key, sub in obj.__dict__.items():
        if key.startswith("_") and key != "__init__":
            continue
        if not sub.__doc__ or sub.__doc__.startswith(key):
            if prefix:
                s = f"{prefix}.{key}"
            else:
                s = key
            objects.append(s)
            object_visitor(objects, s, sub)


def handle_comment(node):
    s = ""
    for para in node:
        assert para.tag == "para"

        # return None if deprecated
        xrefsect = para.find("xrefsect")
        if xrefsect is not None:
            xreftitle = xrefsect.find("xreftitle").text
            if xreftitle == "Deprecated":
                return None
            if xreftitle == "Todo":
                continue

        parameterlist = para.find("parameterlist")
        if parameterlist is not None:
            s += "Parameters\n" + "-" * len("Parameters") + "\n"
            for parameteritem in parameterlist:
                assert parameteritem.tag == "parameteritem"
                parameternamelist = parameteritem[0]
                assert parameternamelist.tag == "parameternamelist"
                name = "".join(parameternamelist.itertext()).strip()
                parameterdescription = parameteritem[1]
                assert parameterdescription.tag == "parameterdescription"
                description = "".join(parameterdescription.itertext()).strip()
                s += f"{name}:"
                for line in description.split("\n"):
                    s += f"\n    {line}"
        else:
            s += "".join(para.itertext()).strip()
        if s and not s.endswith("."):
            s += "."
        s += "\n\n"
    return s


def handle_docs(node):
    brief = node.find("briefdescription")
    brief = handle_comment(brief)
    detail = node.find("detaileddescription")
    detail = handle_comment(detail)
    if brief is None or detail is None:
        return None
    return f"{brief}{detail}".strip()


def handle_compounddef(results, node):
    compoundname = node.find("compoundname").text
    prefix = "HepMC3::"
    if compoundname.startswith(prefix):
        compoundname = compoundname[len(prefix) :]
    # for nested classes
    compoundname = compoundname.replace("::", ".")
    results[compoundname].append(handle_docs(node))
    for ch in node:
        if ch.tag in (
            "compoundname",
            "includes",
            "location",
            "listofallmembers",
            "collaborationgraph",
            "inheritancegraph",
            "briefdescription",
            "detaileddescription",
            "derivedcompoundref",
            "basecompoundref",
            "templateparamlist",
            "innerclass",
        ):
            continue
        if ch.tag == "sectiondef":
            sectiondef = ch
            for ch in sectiondef:
                if ch.tag != "memberdef":
                    continue
                if ch.attrib["prot"] != "public":
                    continue
                n = ch.find("name").text
                if n.startswith("~"):
                    continue
                member = f"{compoundname}.{n}"
                d = handle_docs(ch)
                if d:
                    results[member].append(d)
        else:
            print("unexpected", compoundname, ch)
            breakpoint()


results = defaultdict(list)
for fn in Path("docs/xml").glob("*.xml"):
    if "HepMC3_1_1" not in fn.stem:
        continue
    tree = ET.parse(fn)
    root = tree.getroot()

    for node in root:
        if node.tag == "compounddef":
            handle_compounddef(results, node)
        else:
            print("unexpected", node)
            breakpoint()

# postprocessing: constructors and delta_* methods
for name in list(results):
    p = name.split(".")
    if len(p) > 1:
        if p[-1] == p[-2]:
            p[-1] = "__init__"
        if p[0] == "FourVector" and p[1].startswith("delta_"):
            p = p[1:]
    comment = results[name]
    del results[name]
    name = ".".join(p)
    results[name] = comment

# filter entries
for name in list(results):
    if (
        "Attribute" in name
        or "operator" in name
        or name in IGNORED
        or name.split(".")[0] in IGNORED
    ):
        del results[name]

# join set/get entries into properties
for name in list(results):
    if ".set" not in name:
        continue
    i = name.find(".set")
    i += 4
    try:
        char = name[i]
    except IndexError:
        continue
    if char.islower():
        continue
    setter = name
    if char == "_":
        prop = setter.replace(".set_", ".")
        getter = setter.replace(".set_", ".get_")
    else:
        prop = setter.replace(".set", ".").lower()
        getter = setter.replace(".set", ".get")
    if getter not in results:
        getter = prop
    if getter not in results:
        continue
    results[prop] = results[getter] + results[setter]
    del results[getter]
    del results[setter]

# merge trivially duplicated entries
for name, comment in results.items():
    if len(comment) > 1:
        # strip comments regarding constness
        for i, c in enumerate(comment):
            for x in (" (non-const)", " (const version)", " (const)"):
                if x in c:
                    comment[i] = c.replace(x, "")
                    break
        # unify get/set
        for i, c in enumerate(comment):
            for x in ("Get/set", "Get", "Set"):
                if x in c:
                    comment[i] = c.replace(x, "Access")
                    break
        # merge comments if they are the same
        if comment[0].lower().strip(".") in comment[1].lower():
            comment = comment[:1]

    results[name] = comment

# must import only after _autodoc.py was cleared
import pyhepmc  # noqa

objects = []
object_visitor(objects, "", pyhepmc)

autodoc = cdir / "src" / "pyhepmc" / "_autodoc.py"
with open(autodoc, "w") as f:
    fw = f.write

    fw("# DO NOT EDIT: created by generate_docs.py\n")
    fw("# flake8: noqa\n")
    fw("autodoc = {\n")
    for name in sorted(results):
        if name not in objects:
            print("Info", name, "not found in Python")

        comment = results[name]
        s = "\n\n".join(comment)
        if len(comment) > 1:
            print("WARN", name, "MULTIPLE comments")
        fw(f'    "{name}": """{s}""",\n')
    fw("}\n")
