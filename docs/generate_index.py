# Generate about.rst from README.rst: must change paths to images
with open("../README.rst") as f:
    content = f.read()

content1 = content.replace("image:: docs/", "image:: ./")

with open("index.rst.in") as f:
    content2 = f.read()

with open("index.rst", "w") as f:
    f.write(content1 + "\n\n")
    f.write(content2)
