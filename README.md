# unpywall - Interfacing the Unpaywall API with Python

[![codecov.io](https://codecov.io/gh/naustica/unpywall/branch/master/graph/badge.svg)](https://codecov.io/gh/naustica/unpywall?branch=master)

## Introduction

unpywall is a Python client that utilize the [Unpaywall REST API](https://unpaywall.org/products/api) for scholarly analysis with [pandas](https://pandas.pydata.org/).

This package is influenced by [roadoi](https://github.com/ropensci/roadoi), a R client that interacts with the Unpaywall API.

## Install

Install from [pypi](https://pypi.org/project/unpywall/) using pip:
```python
pip install unpywall
```

## Use

Use the `get` method to query the Unpaywall API. In order to interface the API, your email must be included. The method returns a pandas DataFrame.

```python
from unpywall import Unpywall

Unpywall.get(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
             email='nick.haupka@gmail.com')
```

By setting the parameter progress to True, you can monitore the progress of your API call.

```python
Unpywall.get(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
             email='nick.haupka@gmail.com',
             progress=True)
```

Keep in mind that network errors can occur. Change the errors parameter to `ignore` to avoid a script abort.

```python
Unpywall.get(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
             email='nick.haupka@gmail.com',
             errors='ignore')
```

## Develop

To install unpywall, along with dev tools, run:

```python
pip install -e .[dev]
```
