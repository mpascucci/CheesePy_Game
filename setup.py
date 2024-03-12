from setuptools import setup, find_namespace_packages

setup(
    name='cheesepy_game',
    version='1.1.2',
    url='',
    author='Marco Pascucci',
    author_email='marpas.paris@gmail.com',
    description='A pedagocig python game with mouse and cheese',
    install_requires=[
        "numpy>=1.22.4",
        "pygame>=2.5.2",
        "labyrinth-py==1.0.4"
    ],
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["*.png", "*.ppm"]},
    include_pagekage_data=True
)
