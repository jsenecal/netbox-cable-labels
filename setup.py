from setuptools import find_packages, setup
import codecs
import os.path

with open("README.md", encoding="UTF-8") as readme_file:
    readme = readme_file.read()


def read(rel_path):
    """Read the specified file."""
    path = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(path, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path) -> str | None:
    """Get the version from the specified file."""
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")


setup(
    author="Jonathan Senecal",
    author_email="contact@jonathansenecal.com",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    name="netbox_cable_labels",
    version=get_version("netbox_cable_labels/__init__.py") or "unknown",
    description="Plugin for NetBox that automatically adds labels to cables based on a user defined template",
    license="Apache 2.0",
    install_requires=[],
    packages=find_packages(include=["netbox_cable_labels", "netbox_cable_labels.*"]),
    include_package_data=True,
    zip_safe=False,
)
