from setuptools import find_packages, setup

setup(
    name="auto_cable_label",
    version="0.1",
    description="Plugin for NetBox that automatically adds labels to cables based on the ANSI/TIA-606 Standards",
    author="Jonathan Senecal <contact@jonathansenecal.com>",
    license="Apache 2.0",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
