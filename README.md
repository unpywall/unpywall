# unpywall - Interfacing the Unpaywall API with Python

[![Build Status](https://travis-ci.org/unpywall/unpywall.svg?branch=master)](https://travis-ci.org/github/unpywall/unpywall)
[![codecov.io](https://codecov.io/gh/unpywall/unpywall/branch/master/graph/badge.svg)](https://codecov.io/gh/unpywall/unpywall?branch=master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/unpywall)](https://pypi.org/project/unpywall/)
[![License](https://img.shields.io/github/license/unpywall/unpywall)](https://github.com/unpywall/unpaywall-python/blob/master/LICENSE.txt)
[![PyPI - Version](https://img.shields.io/pypi/v/unpywall)](https://pypi.org/project/unpywall/)

## Introduction

unpywall is a Python client that utilizes the [Unpaywall REST API](https://unpaywall.org/products/api) for scholarly analysis with [pandas](https://pandas.pydata.org/). This package is influenced by [roadoi](https://github.com/ropensci/roadoi), a R client that interacts with the Unpaywall API.

You can find more about the Unpaywall service here: https://unpaywall.org/.

The documentation about the Unpaywall REST API is located here: https://unpaywall.org/products/api.


## Install

Install from [pypi](https://pypi.org/project/unpywall/) using pip:
```python
pip install unpywall
```

## Use

### Authentication

To use the Unpaywall Service, you need to authenticate yourself. For that, unpywall offers multiple ways for authorizing the client. You can either import `UnpywallCredentials` which generates an environment variable or you can set the environment variable by yourself.

```python
from unpywall.utils import UnpywallCredentials

UnpywallCredentials('nick.haupka@gmail.com')
```

Notice that the environment variable for authentication needs to be called `UNPAYWALL_EMAIL`.

```bash
export UNPAYWALL_EMAIL=nick.haupka@gmail.com
```

### Pandas Integration

unpywall uses the data analysis tool [pandas](https://pandas.pydata.org/) for evaluating informations from Unpaywall. By default, the Unpaywall API returns a JSON data structure. However, by using `get_df`, you can transform that into a pandas DataFrame. This also works with multiple DOIs.

```python
from unpywall import Unpywall

Unpywall.get_df(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'])
```

You can track the progress of your API call by setting the parameter `progress` to True. This is especially useful for estimating the time required.

```python
Unpywall.get_df(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
                progress=True)
```

The method also allows two options for catching errors (`raise` and `ignore`)

```python
Unpywall.get_df(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
                errors='ignore')
```

## Develop

To install unpywall, along with dev tools, run:

```python
pip install -e .[dev]
```
