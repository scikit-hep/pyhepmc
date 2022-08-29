# Generate about.rst from README.rst: must change paths to images
with open("../README.rst") as f:
    content = f.read()

content = content.replace("image:: docs/", "image:: ./")

with open("about.rst.in", "w") as f:
    f.write(content)
