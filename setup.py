from __future__ import annotations

from setuptools import setup

with open("README.txt", encoding="utf8") as f:
    README = f.read()

setup(
    name="randrep",
    version="1.0.0",
    description="Pseudorandom, 100% reproducible variable generators",
    url="https://github.com/RealA10N/randrep",
    python_requires=">=3.7,<4",
    long_description=README,
    long_description_content_type="text/plain",
    author="Alon Krymgand",
    author_email="os@alon.kr",
    py_modules=["randrep"],
)
