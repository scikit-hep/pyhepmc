import unicodeit
from particle import Particle
import pprint
import re

table = {}
for p in Particle.findall():
    latex = p.latex_name
    m = re.search(r"(.*?)\\mathrm\{(.+?)\}(.*?)", latex)
    if m:
        latex = m.group(1) + m.group(2) + m.group(3)
    latex = latex.replace(r"^{\prime}", "'")
    latex = latex.replace(r"^{\prime-}", "'^{-}")
    latex = latex.replace(r"^{\prime+}", "'^{+}")
    latex = latex.replace(r"^{\prime0}", "'^{0}")
    latex = latex.replace(r"_{\mu}", r"(\mu)")
    latex = latex.replace(r"_{\tau}", r"(\tau)")
    latex = latex.replace(r"_{\tau'}", r"(\tau')")
    latex = latex.replace(r"_{\mu}", r"(\mu)")
    latex = latex.replace(r"^{*}", r"*")
    latex = latex.replace(r"^{*0}", r"*^{0}")
    latex = latex.replace(r"^{*+}", r"*^{+}")
    latex = latex.replace(r"^{*-}", r"*^{-}")
    latex = latex.replace(r"_{b}", "(b)")
    latex = latex.replace(r"_{c}", "(c)")
    latex = latex.replace(r"_{L}", "(L)")
    latex = latex.replace(r"_{S}", "(S)")
    latex = latex.replace(r"_{c0}", "(c0)")
    latex = latex.replace(r"_{b0}", "(b0)")
    latex = latex.replace(r"_{b1}", "(b1)")
    latex = latex.replace(r"_{c1}", "(c1)")
    latex = latex.replace(r"_{b2}", "(b2)")
    latex = latex.replace(r"_{c2}", "(c2)")
    name = p.name
    u = unicodeit.replace(latex)
    if not ("_" in u or "{" in u):
        table[int(p.pdgid)] = u
    else:
        print(name, latex, u)

s = pprint.pformat(table)

with open("src/pyhepmc/_prettify.py", "w") as f:
    f.write("db = " + s)
