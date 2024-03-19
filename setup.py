from setuptools import setup, find_namespace_packages

setup(
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["*.png", "*.ppm"]},
    include_pagekage_data=True
)
