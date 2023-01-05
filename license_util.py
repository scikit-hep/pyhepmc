from contextlib import contextmanager


@contextmanager
def merge_license_files():
    """
    Merge LICENSE.txt and LICENSES_bundled.txt for sdist creation.

    This follows the approach of Scipy and is to keep LICENSE in repo as an
    exact BSD 3-clause, to make GitHub state correctly how pyhepmc is licensed.
    """

    l1 = "LICENSE"
    l2 = "LICENSES_bundled"

    with open(l1, "r") as f:
        content1 = f.read()

    with open(l2, "r") as f:
        content2 = f.read()

    with open(l1, "w") as f:
        f.write(content1 + "\n\n" + content2)

    yield

    with open(l1, "w") as f:
        f.write(content1)
