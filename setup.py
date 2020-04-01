from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__),"README.md")
with open(readme_path, "r") as handle:
    README = handle.read()

setup(
    name="unpaywallpython",
    version="0.0.1",
    description="Programmatically access open access (OA) articles",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bganglia/unpaywall-python",
    author="bganglia",
    author_email="bganglia892@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages()
)
