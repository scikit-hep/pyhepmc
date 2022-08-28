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
    "Print",
    "Print.line",
    "GenParticlePtr_greater",
    "pair_GenVertexPtr_int_greater",
    "GenEvent.particles",
    "ReaderPlugin",
    "WriterPlugin",
    "Reader",
    "Writer",
    "FourVector.set",
    "FourVector.set_component",
    "FourVector.get_component",
    "FourVector.delta_phi",
    "FourVector.delta_eta",
    "FourVector.delta_rap",
    "FourVector.delta_r2_eta",
    "FourVector.delta_r_eta",
    "FourVector.delta_r2_rap",
    "FourVector.delta_r_rap",
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
            s += "".join(para.itertext()).strip().capitalize()
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

# postprocessing of constructors
tmp = {}
for name, comment in results.items():
    p = name.split(".")
    if len(p) > 1:
        if p[-1] == p[-2]:
            p[-1] = "__init__"
    name = ".".join(p)
    tmp[name] = comment

# filter entries
delete = set()
for name, comment in tmp.items():
    if "Attribute" in name or "operator" in name:
        delete.add(name)
    if name in IGNORED or name.split(".")[0] in IGNORED:
        delete.add(name)
for x in delete:
    del tmp[x]

# join set/get entries into properties
delete = []
tmp2 = {}
for name, comment in tmp.items():
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
    if getter not in tmp:
        getter = prop
    if getter not in tmp:
        continue
    tmp2[prop] = tmp[getter] + tmp[setter]
    delete.append(getter)
    delete.append(setter)

for x in delete:
    del tmp[x]
tmp.update(tmp2)

# merge entries
results = {}
for name, comment in tmp.items():
    if len(comment) > 1:
        # merge comments if they are the same
        if comment[0].lower().strip(".") in comment[1].lower():
            comment = comment[:1]
        # keep non-const when const and non-const are available
        elif "const" in comment[0] and "const" in comment[1]:
            for c in comment:
                if " (non-const)" in c:
                    comment = [c.replace(" (non-const)", "")]
                    break
    results[name] = comment

# must import only after _autodoc.py was cleared
import pyhepmc  # noqa

objects = []
object_visitor(objects, "", pyhepmc)

with open(cdir / "src" / "pyhepmc" / "_autodoc.py", "w") as f:
    fw = f.write

    fw("# DO NOT EDIT: created by generate_docs.py\n")
    fw("# flake8: noqa\n")
    fw("autodoc = {\n")
    for name in sorted(results):
        if name not in objects:
            print("Info", name, "not found in Python")
            continue

        comment = results[name]
        s = "\n\n".join(comment)
        if len(comment) > 1:
            print("WARN", name, "MULTIPLE comments")
        fw(f'    "{name}": """{s}""",\n')
    fw("}\n")
