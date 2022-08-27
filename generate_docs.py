from pathlib import Path  # noqa
import pyhepmc
import subprocess as subp
import xml.etree.ElementTree as ET

if not Path("docs/xml").exists():
    subp.check_call(["doxygen", "docs/Doxyfile"])


def select(root, condition, *tags):
    result = []
    for tag in tags:
        for item in root.iter(tag):
            if condition(item):
                result.append(item)
    return result


def visitor(objects, prefix, obj):
    if not hasattr(obj, "__dict__"):
        return

    for key, sub in obj.__dict__.items():
        if key.startswith("_"):
            continue
        if not sub.__doc__:
            if prefix:
                s = f"{prefix}.{key}"
            else:
                s = key
            objects.append(s)
            visitor(objects, s, sub)


objects = []
visitor(objects, "", pyhepmc)

# for x in sorted(objects):
#     print(x)
print("# DO NOT EDIT: created by generate_docs.py")
print("# flake8: noqa")
print("from pyhepmc import (\n", end="")
for x in sorted(objects):
    if "." in x:
        continue
    print("   " + x, end=",")
print(")")

skip = len("HepMC3::")
for fn in Path("docs/xml").glob("*.xml"):
    if "HepMC3_1_1" not in fn.stem:
        continue
    tree = ET.parse(fn)
    root = tree.getroot()
    parent_map = {c: p for p in tree.iter() for c in p}
    for item in select(
        root,
        lambda x: x.text.startswith("HepMC3::"),
        "compoundname",
    ):
        s = item.text[skip:]
        if s not in objects:
            continue
        par = parent_map[item]
        comment = []
        for child in par:
            if child.tag in ("briefdescription", "detaileddescription"):
                for para in child:
                    assert para.tag == "para"
                    comment.append("".join(para.itertext()) + "\n\n")
        comment = "".join(comment).strip()
        if not comment.endswith("."):
            comment += "."
        print(f'{s}.__doc__ = """{comment}"""\n')
