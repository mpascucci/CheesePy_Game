from setuptools import setup, find_namespace_packages

setup(
    install_requires=[
        "numpy>=1.22.4",
        "pygame>=2.5.2",
        "labyrinth-py>=1.0.4"
    ],
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["*.png", "*.ppm"]},
    include_pagekage_data=True
)
