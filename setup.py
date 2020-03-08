from setuptools import setup
import os

readme_path = os.path.join(os.path.dirname(__file__),"README.md")
with open(readme_path) as handle:
    README = handle.read()

setup(
    name="unpaywall-python",
    version="0.0.1",
    description="Programmatically access open access (OA) articles",
    long_description="README",
    long_description_content_type="text/markdown",
    url="",
    author="bganglia",
    author_email="bganglia892@gmail.com",
    license="MIT",
    classifiers=[],
    packages=[]
)
